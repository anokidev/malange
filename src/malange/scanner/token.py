"""

    malange.scanner.token

    This is the token class.

    Copyright (c) 2024, All right reserved.
    This software is licensed in MIT License.

"""

class TokenClass:
    """This is the main token class."""

    def __init__(self, token: str, position: int):
        self.char: str         = token
        self.position: int     = position


    def __call__(self):
        pass

    def _(self) -> None:
        """
            Process the token.

            Here are the list of token:

            Note:
            - No brackets or parentheses: A token.
            - Square bracket:             A token category.
            - Parentheses:                A token formation.
            - Pipes:                      A possible formation that is unsure.
            - Tag:                        A super-category.
            - Star:                       Can be multiple.
            - Power:                      Optional.

                <TEMPLATE>

                [MALANGE-DIRECTIVE]
                - OPENING_DIRECTIVE                 [
                - CLOSING_DIRECTIVE                 ]
                - OPENING_SLASH_DIRECTIVE           [/
                - CLOSING_SLASH_DIRECTIVE           /]
                - OPENING_SUBDIRECTIVE              {
                - CLOSING_SUBDIRECTIVE              }
                - DIRECTIVE_SEPERATOR               ::
                - DIRECTIVE_ID                      script, match, cond, iterate
                - |DIRECTIVE_ATTR|                  depends on the DIRECTIVE_ID
                - |DIRECTIVE_CONTENT|               depends on the DIRECTIVE_ID and the type of directive
                - |SUBDIRECTIVE_ATTR|               depends on the DIRECTIVE_ID

                (SHORT_DIRECTIVE)
                - OPENING_DIRECTIVE
                - DIRECTIVE_ID
                - DIRECTIVE_SEPERATOR
                - |DIRECTIVE_ATTR|
                - CLOSING_SLASH_DIRECTIVE

                (LONG DIRECTIVE)
                - OPENING DIRECTIVE
                - DIRECTIVE_ID
                - DIRECTIVE_SEPERATOR
                - |DIRECTIVE_ATTR|
                - CLOSING DIRECTIVE
                - |DIRECTIVE_CONTENT|
                - OPENING_SLASH_DIRECTIVE
                - DIRECTIVE_ID
                - CLOSING_SLASH_DIRECTIVE

                (SUBDIRECTIVE)
                - OPENING_SUBDIRECTIVE
                - |SUBDIRECTIVE_ATTR|
                - CLOSING_SUBDIRECTIVE

                |DIRECTIVE_ATTR|
                match DIRECTIVE_ID:
                case script:
                    if __formation__ == (SHORT_DIRECTIVE):
                        DIRECTIVE_ATTR = <PYTHON_CODE>
                    elif __formation__ == (LONG DIRECTIVE):
                        DIRECTIVE_ATTR = NULL
                case cond:
                    if __formation__ == (SHORT_DIRECTIVE):
                        DIRECTIVE_ATTR = * |PYTHON_COMPARISON| PYTHON_PUNCTUATOR_SEMICOLON
                                         |HTML_ELEMENT| PYTHON_PUNCTUATOR_COMA^ "if last item" *
                                         ^ PYTHON_KEYWORD_ELSE PYTHON_PUNCTUATOR_SEMICOLON |HTML_ELEMENT| ^
                    elif __formation__ == (LONG_DIRECTIVE):
                        DIRECTIVE_ATTR = None
                case match:
                    if __formation__ == (SHORT_DIRECTIVE):
                        DIRECTIVE_ATTR = * [PYTHON_LITERALS] PYTHON_PUNCTUATOR_SEMICOLON |HTML_ELEMENT| 
                                         PYTHON_PUNCTUATOR_COMA^ "if last item"*
                    elif __formation__ == (LONGDIRECTIVE):
                        DIRECTIVE_ATTR = None
                case each:
                    if __formation__ == (SHORT_DIRECTIVE):
                        DIRECTIVE_ATTR = PYTHON_ID PYTHON_KEYWORD_IN PYTHON_OBJECT ? |PYTHON_STATEMENT|


                [HTML-TAG]
                - OPENING_TAG                       <
                - CLOSING_TAG                       >
                - OPENING_SLASH_TAG                 </
                - CLOSING_SLASH_TAG                 />
                - TAG_ID                            all html tags except <script> tag
                                                    custom .mala components
                - TAG_ATTRIBUTE                     depends on the TAG_ID
                - TAG_CONTENT                       depends on the TAG_CONTENT

                - Subdirectives:    { ... }        -> Must be inside a long directive.
            - HTML tag tokens:
                - Block tag:        <x> ... </x>
                - Solo tag:         <x>
                - Self-closing tag: <x/>
            - Python code:
                - Recognize only:
                    - The initial 4 space indentation.
                    - The special '$' mark for reactive variables.
        """

    def __str__(self) -> str:
        return ""
