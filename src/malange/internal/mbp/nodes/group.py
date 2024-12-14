'''

    malange.internal.mbp.nodes.group

    The class for group content.

'''

from typing import cast

from .base import MBPContent, MBPBlock
from .for_in import ForBlock
##### from .if_else import IfBlock
from .script import ScriptBlock
##### from .switch import SwitchBlock

from ..processor.lexer import MBPTokenizer, MBPLexer

class GroupContent(MBPContent):
    '''Child class for group elements.'''

    def __init__(self, content: str, layer: int):
        super().__init__(layer)
        self.__process_group(content)

    def __process_group(self, content: str):
        '''Process the data.'''

        self.properties = []

        # Get the tokens.
        tokens: list[MBPTokenizer] = MBPLexer(content).tokens

        # Then, begin identifying a block.
        # A block must be complete:
        # [/bla args::: -> Complete start and end tokens are a start block.
        #   ...
        # /]
        current_layer: int          = 0
        expected_closed_tokens: int = 0

        # Everytime a block is initialized inside a block, the layer
        # goes up. If the layer is 4, then four closing token /] are
        # expected. Everytune /] is discovered, minus 1 to the layer,
        # block only goes +1 if the layer is 0 (aka most upper level).

        # Everytime a block goes +1, the associated start, end, and
        # closing tokens are stored into a block, then added into a list.
        # To do this, the valid start and end tokens are joined into a tuple,
        # then stored in the possibly_valid_start_blocks IF THE LAYER IS 0
        # (so nested start and end tokens are ignored, it will be handled
        # later).
        valid_blocks: list[tuple[MBPTokenizer, MBPTokenizer, MBPTokenizer, int]] = []
        possibly_valid_start_blocks: list[MBPTokenizer] = []

        for (i, current_token) in enumerate(tokens):

            # Get the next, triple previous, and prev tokens.
            try:
                next_token = tokens[i+1]
            except IndexError:
                next_token = MBPTokenizer()
            try:
                prev_token = tokens[i-1]
            except IndexError:
                prev_token = MBPTokenizer()

            # If the current token is start, we must make sure
            # this current token is part of a proper start block.
            # If the next token is MBP_END, it is valid. If it is not
            # not valid. If the valid start block is in layer 0,
            # it will be added to PVSB. If not, it will be ignored.
            if current_token.type == "MBP_START":
                if next_token.type == "MBP_END":
                    if current_layer == 0:
                        possibly_valid_start_blocks = [
                            current_token, next_token]
                    expected_closed_tokens += 1
                else:
                    raise

            # If the current token is end, if it is another MBP_START,
            # increase the layer (because now it is nesting). But raise
            # the expected closed tokens by one.
            elif current_token.type == "MBP_END":
                if next_token.type == "MBP_START":
                    current_layer += 1
                elif next_token.type == "MBP_CLOSE":
                    pass
                elif next_token.type in ("MBP_END", None):
                    raise
                else:
                    raise

            # If the current token is closed, check if the previous is an opening 
            # block, if it is then create a valid block if it is a layer 0 block.
            # If it is a non-zero (nested) block, then pass. After that lower the
            # expected_closed_tokens by one.
            elif current_token.type == "MBP_CLOSED":
                if prev_token.type == "MBP_END":
                    if current_layer == 0:
                        pvsb = possibly_valid_start_blocks
                        try:
                            valid_blocks.append((pvsb[0], pvsb[1],
                                current_token, self.LAYER + current_layer))
                        except IndexError:
                            raise
                        possibly_valid_start_blocks = []
                        expected_closed_tokens -= 1
                    else:
                        expected_closed_tokens -= 1
                elif next_token.type == "MBP_CLOSED":
                    expected_closed_tokens -= 1
                else:
                    raise

        # Now, with the list of valid blocks finished. Time to get the contents.
        for (index, (start, end, close, layer)) in enumerate(valid_blocks):

#####            # Need to create a duct-tape solution, im too sleepy.
            # PyRight constantly complained about start.end being None
            # even tho all tokens with its properties set to None have been
            # purged.
            if start.end != None and start.start != None and end.start != None and end.end != None:
                ref_start: int       = cast(int, start.end)
                ref_end_start: int   = cast(int, end.start)
                ref_end_end: int     = cast(int, end.end)
                ref_close_start: int = cast(int, close.start)
            else:
                raise

            # We need to obtain the block name + args.
            block_name_args = content[ref_start+1:ref_end_start]
            # Get the name.
            block_name = block_name_args.split()[0]
            # Get the args.
            block_args = block_name_args.lstrip(block_name)
            # Get the content.
            block_content = content[ref_end_end+1:ref_close_start]

            if block_name == "script":
                self.properties.append(ScriptBlock(block_content, block_args, int(layer)))
            elif block_name == "for":
                self.properties.append(ForBlock(block_content, block_args, layer))
            elif block_name == "if":
                pass
#####           self.properties.append(IfBlock(block_content, block_args, layer))
            elif block_name == "switch":
                pass
#####           self.properties.append(SwitchBlock(block_content, block_args, layer))
            else:
                raise

            # Get the inter-block contents, if there are any.
#####            # If you notice the duct-tape solution sorry.
            try:
                next_block = valid_blocks[index+1]
                if close.end != None and next_block[0].start != None:
                    ref_close_end  = close.end
                    ref_next_start = next_block[0].start
                else:
                    raise
                inter_content = content[ref_close_end+1:ref_next_start]
            except IndexError:
                if close.end != None:
                    ref_close_end = close.end
                else:
                    raise
                inter_content = content[ref_close_end+1:]

            # Add the inter_content as a HTML Content.
#####            if not inter_content:
#####               self.CONTENT.append(process_html(inter_content))
