"""

    malange.lexer.element

    The lexer for element, the foundational
    block of malange syntax.

    Copyright (c) 2024 Anoki Youssou,
    all right reserved. Licensed in
    MIT License.

"""

import re
import typing

class ElementLexer:

    def begin_analyzing(self, text: str):

        # Save the text in the instance class.
        self.__text = text

        # Parse the text first.
        self.__parse_text()

    def __parse_text(self) -> None:
        """Deconstruct the text into a series of element identifiers."""

        # Check for the existence of a square brackets.
        self.__token_dict: typing.Union[
            dict[str, list[re.Match[str]]], dict[str, None]
        ] = {}

        # Here are the list of characters that are detected (the identifiers):
        regex_1 = r"[\[\]]|"         # [ and ]
        regex_2 = r"[<>]"            # < and >
        regex_3 = r"[\(\)]|"         # ( and )
        regex_4 = r"(\[\/)|(<\/)|"   # [/ and </
        regex_5 = r"(\/\])|(\/>)|"   # /] and />

        for index, content in enumerate(self.__text.splitlines()):
            # But first, we need to remove empty lines.
            if content != "":
                # Then, we began filtering out using regex. The order of re matters!!!
                self.__token_dict[f'{str(index+1)}'] = [i for i in re.finditer(
                    regex_3 + regex_4 + regex_5 + regex_1 + regex_2, content)]

        # For the purpose of practicality, we will make the simple version of token_dict.
        # Which is a dictionary. The key refers to the line num, while the content is a
        # list that are composed of a token, the token is a tuple that are composed of the
        # data of the token and the location of the token.
        # Like this: '1' : [ ('[', (0, 1)) , ...]

        self.__simple_token: dict[str, list[tuple[str, int]]] = {}

        for index, content in self.__token_dict.items():
            # i.group() = The identifier, i.start() = The index/location.
            self.__simple_token[index] = [(i.group(), i.start()) for i in content]

    def __analyze_identifiers(self) -> None:
        """Begin analyzing the identifiers."""

        # Here's how it works.
        #
        # First, we need to know the role of the indentifiers:
        # To be valid, any identifier must be part of a pair.
        # The pair is like '[ ... ]', or '< ... >', or '</ ... >',
        # you get it.

        # '[', and '<' are the beginning of the opening pair of short/long block.
        # '[/' and '</' are the beginning of the closing pair of long block.
        # ']' and '>' are the ending of opening and closing pair of long block &
        # html elements that doesn't self-close e.g. meta tag.
        # '/>' and '/]' are the ending of short block.
        # '(' and ')' are beginning and ending of subdirective.

        # Now, here is what we are going to do, we are going to loop
        # self.__simple_token. Then we are going to do this:
        #
        # - Identify the pairs. Any invalid identifier is immediately marked as an error.
        # For example, this is valid: < ... >, </ ... >, [ ... ], [/ ... ], ( ... )
        # - Begin nesting hierarchy analysis: If an opening pair is found, the next pair should
        # be closing. If not, then that means there is a nesting. But, then two closing pairs are
        # expected (to complete the element). Not only that, several direc pair doesn't accept nesting.
        # - Identify if the pairs type are invalid. This is valid:
        # <..> ... </..>, [..] .. [/..]
        # - Then identify if the nesting is valid or not.


        # Also, there are exceptions:
        #
        # 1. There is a thing called short directive that doesn't have closing pair,
        # and has a special ending identifier /].
        # 2. There are self-closing HTML tags (<img/>), and non self-closing 
        # HTML tags that doesn't have a closing pair, such as <meta>
        # 3. Subdirectives can only being nested inside long directives.
        # 4. Several long direc don't except tag element being nested inside them,
        # such as the [script] directive. Contents inside script direc are Python code.
        # 5. All short direc nest tag elements INSIDE the pair.

        for line_num, token in self.__simple_token.items():
            for char, location in token:
                """TO BE CONTINUED!!!!"""

