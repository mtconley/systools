import traceback as tb

def get_stack():
    return tb.extract_stack()

def parse_stack_entry(entry):
    file_, line_, in_, code_ = entry
    data = {'file': file_,
           'line': line_, 
           'in': in_,
           'code': code_}
    return data

def format_stack_entry(stack_entry, depth):
    string = \
    """Call Depth: {0}
        File: {1}
        Line: {2} in {3}
        Code:
            {4}""".format(depth, *stack_entry)
    return string

def parse_stack(stack):
    result = {}
    for ix, entry in enumerate(stack):
        result[ix] = parse_stack_entry(entrya)
    return result

def print_last_call():
    entry = get_stack()[-1]
    print format_stack_entry(entry, 0)

def print_stack(stack=None):
    stack = stack if stack else get_stack()
    nEntry = len(stack)
    for ix, entry in enumerate(stack):
        ix = nEntry - ix
        print format_stack_entry(entry, ix)