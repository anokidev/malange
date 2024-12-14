'''

    malange.internal.mbp.nodes.base

    Containing the base, which will form the bases of Malange AST.

'''

class MBPBlock:
    '''The base class for blocks, one of the many node types in MBP AST.'''
    def __init__(self, layer: int):
        self.CONTENT      = None
        self.ARGUMENT     = None
        self.LAYER        = layer + 1

class MBPArgument:
    '''The base class for arguments, one of the many node types in MBP AST.'''
    def __init__(self, layer: int):
        self.LAYER        = layer

class MBPContent:
    '''The base class for contents, one of the many node types in MBP AST.'''
    def __init__(self, layer: int):
        self.CONTENT      = None
        self.LAYER        = layer






