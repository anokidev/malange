'''

    malange.internal.mbp.script

    Storing the block class of [/script/]

'''

import re

from .base import MBPBlock

class ScriptBlock(MBPBlock):
    '''Script block.'''

    def __init__(self, content: str, args: str, layer: int):
        super().__init__(layer)
        self.ARGUMENTS = self.__handle_args(args)
#####   # self.CONTENT    = process_code(content, self.layer)

    def __handle_args(self, args: str):
        '''Handle arguments.'''

        # First step is to regex the args.
        backend: list[re.Match[str]] = list(re.finditer(
            r"backend=\(([^)]+)\)", re.sub(r'\s+', '', args)))
        src: list[re.Match[str]] = list(re.finditer(
            r"src=(\S+)", re.sub(r'\s+', '', args)))

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
            self.__backend_package_list: list[str] = backend_package.split(',')
        except IndexError:
            self.__backend_package_list: list[str] = []

        # Fourth step is to check the syntax of src.
        try:
            self.__src_path: str = src[0].group()
            # If the src is like this: '..." or the opposite, error.
            if self.__src_path[0] != self.src_path[-1]:
                raise 
        except IndexError:
            self.src_path: str = ""

        # Save the args.
        class arguments:
            backend = self.__backend_package_list
            src     = self.__src_path
        self.ARGUMENTS = arguments
