'''

    malange.internal.mbp.script

    Storing the block class of [/script/]

'''

import re

from .base import MBPBlock, MBPArgument

class ScriptArgument(MBPArgument):
    '''The class for script arguments.'''

    def __init__(self, layer: int, arg: str):
        super().__init__(layer)

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
        self.backend = self.backend_package_list,
        self.src     = self.src_path

class ScriptBlock(MBPBlock):
    '''Script block.'''

    def __init__(self, content: str, arg: str, layer: int):
        super().__init__(layer)
        self.ARGUMENT = ScriptArgument(self.LAYER, arg)
#####        # self.CONTENT    = process_code(content, self.layer)
