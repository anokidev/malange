'''

    malange.internal.mbp.processor.lexer

    The lexical analysis tool and tokenizer for MBP.

'''

import re
import typing

class MBPTokenizer:
    '''Create MBP tokens for scanning aka lexing.'''

    def __init__(self, result: typing.Union[re.Match[str], None] = None):

        if result is None:
            self.type:  typing.Optional[str] = None
            self.start: typing.Optional[int] = None
            self.end:   typing.Optional[int] = None
        else:
            # Check the text result.
            if result.group() == "[/": # [/ is used for opening block.
                self.type = "MBP_START"
            elif result.group() == "/]": # /] is used for closing block.
                self.type = "MBP_CLOSE"
            elif result.group() == ":::": # Detect if it is an opening block end.
                self.type = "MBP_END"
            elif result.group() == "(/": # Detect if it is an opening sub-block.
                self.type = "MBP_SUBSTART"
            elif result.group == "/)": # Detect if it is a closing sub-block.
                self.type = "MBP_SUBCLOSE"
            elif result.group == ":)":
                self.type = "MBP_SUBEND"
            else: # Anything other than that means a mistake in the REGEX (class MBP), thus an error.
                raise 

            self.start = result.start()
            self.end   = result.end()


class MBPLexer:
    '''The main lexer class.'''

    def __init__(self, text: str):
        '''Scan the code line.'''

        # This is the tokens.
        results: list[re.Match[str]] = list(re.finditer(
            r"(\\\[/)|(\\\:\:\:)|(\\\/\])|(\[\/)|(\:\:\:)|(\/\])", text))
        tokens: list[MBPTokenizer] = []
        for result in results:
            # Escaped elements are skipped.
            if result.group() in (r"\:::", r"\[/", r"\/]"):
                pass
            else:
                tokens.append(MBPTokenizer(result))
        self.tokens: list[MBPTokenizer] = tokens

class MBPSubLexer:
    '''The lexer class used for detecting subblocks.'''

    def __init__(self, text: str):
        '''Scan the code line.'''

        # This is the tokens.
        results: list[re.Match[str]] = list(re.finditer(
            r"(\\\(/)|(\\\:\))|(\\\/\))|(\(\/)|(\:\))|(\/\))", text))
        tokens: list[MBPTokenizer] = []
        for result in results:
            # Escaped elements are skipped.
            if result.group() in (r"\:)", r"\(/", r"\/)"):
                pass
            else:
                tokens.append(MBPTokenizer(result))
        self.tokens: list[MBPTokenizer] = tokens


