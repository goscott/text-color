import sys

TEMPLATE = '\033[{}m'
DEFAULTS = None

# available styles
class styles:
    BLACK = '\033[30m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[34m'
    MAGENTA = '\033[95m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    BLACK_BG = '\033[40m'
    RED_BG = '\033[41m'
    GREEN_BG = '\033[42m'
    YELLOW_BG = '\033[43m'
    BLUE_BG = '\033[44m'
    MAGENTA_BG = '\033[45m'
    CYAN_BG = '\033[46m'
    WHITE_BG = '\033[47m'

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALICS = '\033[3m'
    INVERSE = '\033[7m'

    DONE = '\033[0m'

# sets defaults from this point on, until a reset
def set_defaults(sep=None, end=None, file=None, flush=None, reset=None,
        remove_old_styles=None):
    global DEFAULTS
    DEFAULTS = {}
    if sep != None:
        DEFAULTS['sep'] = sep
    if end != None:
        DEFAULTS['end'] = end
    if file != None:
        DEFAULTS['file'] = file
    if flush != None:
        DEFAULTS['flush'] = flush
    if reset != None:
        DEFAULTS['reset'] = reset
    if remove_old_styles != None:
        DEFAULTS['remove_old_styles'] = remove_old_styles

# resets default settings
def remove_defaults():
    global DEFAULTS
    DEFAULTS = None

# functions the same as the default print function, but with a style parameter and
# some other custom options
def cprint(style, *args, sep=' ', end='\n', file=sys.stdout, flush=False,
        reset=True, remove_old_styles=True, override_defaults=False):
    # use default setings
    if not override_defaults and DEFAULTS != None:
        if 'sep' in DEFAULTS:
            sep = DEFAULTS['sep']
        if 'end' in DEFAULTS:
            end = DEFAULTS['end']
        if 'file' in DEFAULTS:
            file = DEFAULTS['file']
        if 'flush' in DEFAULTS:
            flush = DEFAULTS['flush']
        if 'reset' in DEFAULTS:
            reset = DEFAULTS['reset']
        if 'remove_old_styles' in DEFAULTS:
            remove_old_styles = DEFAULTS['remove_old_styles']

    get_style = lambda x: TEMPLATE.format(x) if type(x) == int else x

    # end old styles
    if remove_old_styles:
        print(styles.DONE, end='', sep=sep, file=file, flush=flush)
    # start new style(s)
    if type(style) == list or type(style) == tuple:
        print(''.join([get_style(s) for s in style]),
            end='', sep=sep, file=file, flush=flush)
    else:
        print(get_style(style), end='')
    # print output
    if reset:
        print(*args, sep=sep, end='', file=file, flush=flush)
        print(styles.DONE, end=end)
    else:
        print(*args, sep=sep, end=end, file=file, flush=flush)

# test script
if __name__ == '__main__':
    cprint(styles.MAGENTA, 'This is a magenta four:', 4, end='', reset=False)
    cprint(styles.GREEN, ' and this is green', '(this too)\n')

    set_defaults(reset=False)
    cprint(styles.CYAN, 'something in cyan')
    print('\tStill Cyan!\n')

    cprint(styles.YELLOW, 'will this reset?', reset=True)
    print('\tNope! Reset your defaults!\n')
    cprint(styles.UNDERLINE, 'asdlkfjasdf', reset=True, override_defaults=True)
    print('asdfasdfasdf\n')

    remove_defaults()
    cprint([styles.RED, styles.UNDERLINE], 'red AND underline?!')
    print('No style any more\n')

    cprint(styles.CYAN_BG, 'cyan background\n')

    cprint([styles.RED_BG, styles.YELLOW, styles.UNDERLINE], "LOTS OF STYLES!\n")