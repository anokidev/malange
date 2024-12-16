'''

    malange.internal.mbp.nodes.switch

    Storing the block class of [/switch/]

'''

import re

from .base import MBPBlock, MBPContent
from .tools import check_for_none
from ..processor.lexer import MBPSubLexer, MBPTokenizer

class SwitchContent(MBPContent):
    '''Parse the content of [/if/]'''
    def __init__(self, content: str, layer: int):
        super().__init__(layer)
        self.CONTENT: list[tuple[str, str, str]] = [] # Set the type to a list.
        # Get the (/, /), and :::
        sub_tokens: list[MBPTokenizer] = MBPSubLexer(content).tokens
        self.__process_sub_tokens(content, sub_tokens)

    def __process_sub_tokens(self, content: str, sub_tokens: list[MBPTokenizer]):
        '''Process sub tokens.'''
        # Then, begin identifying a block.
        # A subblock must be complete:
        # (/bla args::: -> Complete start and end tokens are a start block.
        #   ...
        # /)

        # Simpler method, no need for a paragraph long comment.
        valid_blocks: list[tuple[MBPTokenizer, MBPTokenizer, MBPTokenizer]] = []
        for (i, current_token) in enumerate(sub_tokens):
            # Get the next, triple previous, and prev tokens.
            next_token = sub_tokens[i+1] if i + 1 < len(sub_tokens) else MBPTokenizer()
            double_next_token = sub_tokens[i+2] if i + 2 < len(sub_tokens) else MBPTokenizer()
            # Create valid blocks.
            if (current_token.type == "MBP_SUBSTART" and
            next_token.type == "MBP_SUBEND" and double_next_token == "MBP_SUBCLOSE"):
                valid_blocks.append((current_token, next_token, double_next_token))
            else:
                raise

        # Get args and contents.
        for (i, (start_token, end_token, close_token)) in enumerate(valid_blocks):
            # Do the same dirty thing in tool.py.
            start_token_end   = check_for_none(int, start_token.end)
            end_token_start   = check_for_none(int, end_token.end)
            end_token_end     = check_for_none(int, end_token.end)
            close_token_start = check_for_none(int, close_token.start)
            # Get the subblock name, arguments, and content.
            block_args: str = content[start_token_end+1:end_token_start]
            sb_content: str = content[end_token_end+1:close_token_start]
            subblock:   str = block_args.strip()[0]
            args:       str = block_args.lstrip(subblock)
            # Filter invalid subblocks.
            if subblock not in ("default", "case"):
                raise
            # If the subblock is an else, but the index is not the last item, raise.
            if i < len(valid_blocks) - 1 and subblock == "default":
                raise
            # A default subblock can not have an argument.
            if subblock == "default" and re.search(r'\S', args):
                raise
            self.CONTENT.append((subblock, sb_content, args))

class SwitchBlock(MBPBlock):
    '''The main class of [/if/]'''
    def __init__(self, content: str, args: str, layer: int):
        super().__init__(layer)
        if re.search(r'\S', args): # There is no args for switch block.
            raise
        self.ARGUMENTS = args
        self.CONTENT   = SwitchContent(content, layer)
