'''

    malange.internal.mbp.nodes.for_in

    Storing the block class of [/for/]

'''

import re

from .base import MBPArgument, MBPBlock
from .group import GroupContent

class ForArgument(MBPArgument):
    '''For argument.'''

    def __init__(self, arg: str, layer: int):
        super().__init__(layer)

        # Get the matches.
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
        self.indexes   = indexes
        self.iterables = iterables

class ForBlock(MBPBlock):
    '''For block.'''

    def __init__(self, content: str, arg: str, layer: int):
        super().__init__(layer)
        self.ARGUMENT = ForArgument(arg, self.LAYER)
        self.CONTENT = GroupContent(content, self.LAYER)
