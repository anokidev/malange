'''

    malange.internal.mbp.nodes.group

    The class for group content.

'''

from typing import Optional

from .base import MBPContent
from .tools import append_content

from ..processor.lexer import MBPTokenizer, MBPLexer

class RootContent(MBPContent):
    '''Child class for group elements.'''

    def __init__(self, content: str, layer: int):
        super().__init__(layer)
        self.__process_group(content)

    def __process_group(self, content: str):
        '''Process the data.'''
        self.PROPERTIES = append_content(content, self.__create_blocks(content))

    def __create_blocks(self, content) -> Optional[list[tuple[
            MBPTokenizer, MBPTokenizer, MBPTokenizer, int]]]:
        '''Begin creating valid blocks.'''
        # Get the tokens.
        tokens: list[MBPTokenizer] = MBPLexer(content).tokens

        # If you want to know how tihis works read root.py
        # group.py is the same but with token arrangement safety
        # removed since it is not necessary.
        current_layer: int          = 0
        expected_closed_tokens: int = 0
        valid_blocks: list[tuple[MBPTokenizer, MBPTokenizer, MBPTokenizer, int]] = []
        possibly_valid_start_blocks: list[MBPTokenizer] = []

        for (i, current_token) in enumerate(tokens):

            # Get the next, triple previous, and prev tokens.
            next_token = tokens[i+1] if i + 1 < len(tokens) else MBPTokenizer()
            prev_token = tokens[i-1] if i > 0 else MBPTokenizer()

            if current_token.type == "MBP_START":
                if next_token.type == "MBP_END":
                    if current_layer == 0:
                        possibly_valid_start_blocks = [
                            current_token, next_token]
                    expected_closed_tokens += 1
                else:
                    raise

            elif current_token.type == "MBP_END":
                if next_token.type == "MBP_START":
                    current_layer += 1
                elif next_token.type == "MBP_CLOSE":
                    pass
                elif next_token.type in ("MBP_END", None):
                    raise
                else:
                    raise

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
