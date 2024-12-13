from .lexer import MBPLexer, MBPTokenizer

class MBPManager(MBPLexer):
    '''Main manager for MBP.'''

    def __init__(self, code: str):
        # Split the code.
        code_lines: list[str] = code.splitlines()
        # Create tokens.
        self.__tokens: list[MBPTokenizer] = []
        for (num, line) in enumerate(code_lines):
            self.__tokens += self._lexer(num, line)
        # Generate the tree.
        self.__construct_tree()

    def __construct_tree(self) -> None:
        '''Begin constructing a structure tree.'''

        # 0 means root level. The more number, the deeper it go.
        current_layer = 0
        # True means content, False means args.
        current_sec   = True

        for (num, token) in enumerate(self.__tokens):
            if token.type == "MBP_OPENING-BLOCK":
                # False means in args mode, which means MBP_OPENING-BLOCK-END is needed.
                pass

