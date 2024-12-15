'''

    malange.internal.mbp.root

    Storing the content class of root.

'''

from typing import Optional

from .base import MBPContent
from .tools import append_content

from ..processor.lexer import MBPTokenizer, MBPLexer

class RootContent(MBPContent):
    '''Child class for group elements.'''

    def __init__(self, content: str):
        super().__init__(0)
        self.__process_group(content)

    def __process_group(self, content: str):
        '''Process the data.'''
        self.PROPERTIES = append_content(content, self.__create_blocks(content))

    def __create_blocks(self, content) -> Optional[list[tuple[
            MBPTokenizer, MBPTokenizer, MBPTokenizer, int]]]:
        '''Begin creating valid blocks.'''
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
            next_token = tokens[i+1] if i + 1 < len(tokens) else MBPTokenizer()
            prev_token = tokens[i-1] if i > 0 else MBPTokenizer()

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
                elif next_token.type == "MBP_CLOSED":
                    expected_closed_tokens -= 1
                else:
                    raise

            return valid_blocks
