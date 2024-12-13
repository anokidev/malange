'''

    malange.internal.mbp.parser

    Containing parser, which will build AST
    while diagnosing parsing errors.

'''

import re

from .lexer import MBPLexer

class MBPNodes:
    '''Create MBP nodes for AST creation aka parsing.'''

    def __init__(self):
        self.type         = None
        self.content      = None
        self.content_type = None
        self.args         = None

class GroupElement(MBPNodes):
    '''Child class for group elements.'''

    def __call__(self, content: str):
        self.type = "GROUP_ELEMENT"
        self.__process_group(content)

    def __process_group(self, content: str):
        '''Process the data.'''

        self.content_type = "ELEMENT_LIST"
        matches = MBPLexer()(content)

class ScriptBlock(MBPNodes):

    def __call__(self, content: str, arg: str):
        self.type = "SCRIPT_BLOCK"
        self.__process_script(content, arg)

    def __process_script(self, content: str, arg: str) -> None:
        '''Parsing script.'''

        self.content = content
        self.content_type = "PYTHON_CODE"

        self.__parse_args(arg)

    def __parse_args(self, arg: str) -> None:

        # First step is to regex the args.
        backend: list[re.Match[str]] = list(re.finditer(
            r"backend=\(([^)]+)\)", re.sub(r'\s+', '', arg)))
        src: list[re.Match[str]] = list(re.finditer(
            r"src=(\S+)", re.sub(r'\s+', '', arg)))

        # Second step is to ensure that there can only be one backend and one src.
        if len(backend) > 1:
            raise
        if len(src) > 1:
            raise

        # Third step is to check the syntax of backend.
        try:
            backend_package: str = backend[0].group()
            # Check if there are clumped commas.
            if re.search(r",,+", backend_package):
                raise
            # If not, get the package list.
            self.backend_package_list: list[str] = backend_package.split(',')
        except IndexError:
            self.backend_package_list: list[str] = []

        # Fourth step is to check the syntax of src.
        try:
            self.src_path: str = src[0].group()
            # If the src is like this: '..." or the opposite, error.
            if self.src_path[0] != self.src_path[-1]:
                raise 
        except IndexError:
            self.src_path: str = ""

        # Save the args.
        self.args = {
            'backend' : self.backend_package_list,
            'src'     : self.src_path
        }

class ForBlock(MBPNodes):
    '''For block.'''

    def __call__(self, content: str, args: str):
        self.type = "FOR_BLOCK"
        self.__process_args(args)
        self.__process_content(content)

    def __process_args(self, arg) -> None:
        '''Process the arguments.'''

        matches: list[re.Match[str]] = list(re.finditer(r"(\bin\s+\b)", arg))

        # If there is no in, raise.
        if not matches:
            raise
        # If there are multiple in, raise.
        if len(matches) > 1:
            raise
        # Get the indexes and iterables.
        indexes = arg[:matches[0].start()]
        iterables = arg[matches[0].end()+1:]
        # Save it. Whether the data is true depends on Python.
        self.args = {
            'indexes'   : indexes,
            'iterables' : iterables
        }

    def __process_content(self, content) -> None:
        '''Process the content.'''

        self.content = GroupElement()(content)




