import re

from .misc import isboolswitch


def prompt_options(pattern, prompt):

    """Ensure response to prompt matches pattern.
    If pattern is list, literal options will be displayed"""
    if isboolswitch(pattern):
        value = _prompt_bool(prompt)
    elif isinstance(pattern, list):
        value = _list_prompt(pattern, prompt)
    else:
        value = _pattern_prompt(pattern, prompt)
    return value

def _prompt_bool(prompt):
    prompt = "{0} [True/False]: ".format(prompt)
    menu_options = {'t': True, 'f': False}
    choice = raw_input(prompt) or 'f'
    value = menu_options.get(choice.lower()[0], False)
    return value

def _pattern_prompt(pattern, prompt):
    ERROR = '\nInput must match pattern, {0}\n'.format(pattern)
    switch = True    
    while switch:
        value = raw_input(prompt)
        switch = not re.match(pattern, value)
        if switch:
            print ERROR
    return value

def _list_prompt(menu_options, prompt):
    prompt = prompt + '\n  ' + '\n  '.join(menu_options)
    pattern = '|'.join(menu_options)
    ERROR = '\nInput must be in list\n'
    switch = True    
    while switch:
        print prompt
        value = raw_input('> ')
        switch = not re.match(pattern, value)
        if switch:
            print ERROR