'''

    malange.internal.mbp.nodes.for_in

    Storing the block class of [/for/]

'''

import re

from .base import MBPBlock
from .group import GroupContent

class ForBlock(MBPBlock):
    '''For block.'''

    def __init__(self, content: str, args: str, layer: int):
        super().__init__(layer)
        self.ARGUMENTS = self.__handle_args(args)
        self.CONTENT   = GroupContent(content, self.LAYER)

    def __handle_args(self, arg: str):
        '''Handle the arguments.'''

        # Get the matches.
        matches: list[re.Match[str]] = list(re.finditer(r"(\bin\s+\b)", arg))
        # If there is no in, raise.
        if not matches:
            raise
        # If there are multiple in, raise.
        if len(matches) > 1:
            raise
        # Get the indexes and iterables.
        r_indexes = arg[:matches[0].start()]
        r_iterables = arg[matches[0].end()+1:]
        # Save it. Whether the data is true depends on Python.
        class arguments:
            indexes   = r_indexes
            iterables = r_iterables
        return arguments
