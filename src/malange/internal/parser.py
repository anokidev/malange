'''

    malange.internal.parser

    The manager for Malange parser, it will manage:
    - The identification of Malange tokens through internal.mbp
    - The parsing of Python and HTML codes.

'''

from malange.internal.mbp import MBP

class Parser:
    '''This is the main parser manager of Malange.'''

    def __init__(self, code: str):
        self.__code: str = code
        self.__mbt       = MBP()

    def __call__(self):
        self.__primary_tokens = MBP(self.__code)
