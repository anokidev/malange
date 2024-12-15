'''

    malange.internal.mbp.nodes.tools

    A collection of reusable functions used
    by the nodes folder.

'''


from .for_in import ForBlock
##### from .if_else import IfBlock
from .script import ScriptBlock
##### from .switch import SwitchBlock

def check_for_none(typ, thing):
    if thing == None:
        raise
    new = typ(thing)
    return new

def append_content(content, valid_blocks):
    '''Used for root.py and group.py, specifically
    for creating a list of Malange blocks and HTML elements.'''

    PROPERTIES = []

    # Now, with the list of valid blocks finished. Time to get the contents.
    for (index, (c_start, c_end, c_close, c_layer)) in enumerate(valid_blocks):
#####   # Need to create a duct-tape solution, im too sleepy.
        # PyRight constantly complained about start.end being None
        # even tho all tokens with its properties set to None have been
        # purged through a mechanism of try except and if else in the other files.
        # c_start: The [/x, c_end: The :::, The c_close: The /] property
        # start and end refers to the index of the char of start and end respectfully.
        class cr_start:
            start: int = check_for_none(int, c_start.start)
            end:   int = check_for_none(int, c_start.end)
        class cr_end:
            start: int = check_for_none(int, c_end.start)
            end:   int = check_for_none(int, c_end.end)
        class cr_close:
            start: int = check_for_none(int, c_close.start)
            end:   int = check_for_none(int, c_close.end)

        # First, we need to obtain the content between the first block and the start of the file.
        if index == 0:
            before_content: str = content[:cr_start.start]
#####       # PROPERTIES.append(process_html(before_content, c_layer))

        # Then after that we get the content between the opening block and the closing token.
        # We need to obtain the block name + args.
        block_name_args: str = content[cr_start.end+1:cr_end.start]
        # Get the name.
        block_name:      str = block_name_args.split()[0]
        # Get the args.
        block_args:      str = block_name_args.lstrip(block_name)
        # Get the content.
        block_content:   str = content[cr_end.end+1:cr_close.start]

        if block_name == "script":
            PROPERTIES.append(ScriptBlock(block_content, block_args, c_layer))
        elif block_name == "for":
            PROPERTIES.append(ForBlock(block_content, block_args, c_layer))
        elif block_name == "if":
            pass
#####       PROPERTIES.append(IfBlock(block_content, block_args, layer))
        elif block_name == "switch":
            pass
#####       PROPERTIES.append(SwitchBlock(block_content, block_args, layer))
        else:
            raise

        # Get the inter-block contents, if there are any.
#####   # If you notice the duct-tape solution sorry.
        try:
            next_block         = valid_blocks[index+1]
            n_start_start: int = check_for_none(int, next_block[0].start)
            inter_content: str = content[cr_close.end+1:n_start_start]
        # If the block is the last, get the intercontent between the last block and EOF.
        except IndexError:
            inter_content: str = content[cr_close.end+1:]

        # Add the inter_content as a HTML Content.
#####   if not inter_content:
#####       PROPERTIES.append(process_html(inter_content, c_layer))

    return PROPERTIES
