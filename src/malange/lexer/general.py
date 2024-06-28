"""

    malange.lexer.general

    The general lexer analyzer.

    Copyright (c) 2024 Anoki Youssou,
    all right reserved. Licensed in
    MIT License.

"""

import re
from typing import Union

ParsedTextType = Union[dict[str, list[re.Match[str]]], dict[str, None]]

class LexerAnalyzer:
    """This is the lexical analyzer, or the lexer."""

    def __init__(self, text: str) -> None:
        """First, we have to breakdown the text."""

        self.text: list[str] = text.splitlines()

        for i in text:
            self.__feeder(i)

    def __feeder(self, text: str):
        """Feeder will deconstruct a statement."""

        # Check for the existence of a square brackets.
        clean_text: dict[str, str] = {}
        token_dict: ParsedTextType = {}

        # Here are the list of characters that are detected:
        # - [ and ]
        # - < and >
        # - [/ and </

        # But first, we need to remove empty lines.
        for index, content in enumerate(text.splitlines()):
            if content != "":
                clean_text[f'{str(index+1)}'] = content

        # Then we began looking for token list.
        for index, content in clean_text.items():
            token_dict[index] = [i for i in re.finditer(
                r"(\[\/)|(<\/)|[\[\]]|[<>]", content)]

        # For the purpose of practicality, we will make the simple version of token_dict.
        # Which is a dictionary. The key refers to the line num, while the content is a
        # list that are composed of a token, the token is a tuple that are composed of the
        # data of the token and the location of the token.
        # Like this: '1' : [ ('[', (0, 1)) , ...]

        simple_token: dict[str, list[tuple[str, tuple[int, int]]]] = {}

        for index, content in token_dict.items():
            simple_token[index] = [(i.group(), (i.start(), i.end())) for i in content]


