'''

    malange.internal.mbp.lexer

    The lexical analysis tool and tokenizer for MBP.

'''

import re

class MBPTokenizer:
    '''Create MBP tokens for scanning aka lexing.'''

    def __init__(self, result: re.Match[str]):
        # Check the text result.
        if result.group() == "[/": # [/ is used for opening block.
            self.type = "MBP_OPENING-BLOCK-START"
        elif result.group() == "/]": # /] is used for closing block.
            self.type = "MBP_CLOSING-BLOCK"
        elif result.group() == ":::": # Detect if it is an opening block end.
            self.type = "MBP_OPENING-BLOCK-END"
        else: # Anything other than that means a mistake in the REGEX (class MBP), thus an error.
            raise 

        self.start = result.start()
        self.end   = result.end()


class MBPLexer:
    '''The main lexer class.'''

    def __call__(self, text: str):
        '''Scan the code line.'''

        # This is the tokens.
        results: list[re.Match[str]] = list(re.finditer(
            r"(\[\/(^[\/\[\]])\:\:\:)" + r"|(\/\])", text))
        tokens: list[MBPTokenizer] = []
        for result in results:
            # Escaped elements are skipped.
            if result.group() in (r"\:::", r"\[/", r"\/]"):
                pass
            else:
                tokens.append(MBPTokenizer(result))
        self.tokens: list[MBPTokenizer] = tokens

    def form_first_level_hierarchy(self):
        layer = 0 # 0 means the first level, the higher the deeper.
        complete = 0 # Everytime a complete, means a pair of first-level block.
        complete_elements = []
        for i in self.tokens:
            if i.type == "MBP_OPENING_START":


