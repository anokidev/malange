'''

    malange.internal.mbp.root

    Storing the content class of root.

'''

from typing import Optional

from .base import MBPBlock
from .group import GroupContent

class RootBlock(MBPBlock):
    '''Child class for group elements.'''

    def __init__(self, content: str):
        super().__init__(0)
        self.CONTENT = GroupContent(content, self.LAYER)
