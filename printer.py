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

# prints a usage message
def help():
    # basic overview
    cprint('\nTo print in a certain style:', style=styles.INVERSE)
    cprint('\tcprint(style, *args)', style=styles.YELLOW)
    # similarities with "print()"
    cprint('\t\t-',
        cprint("args", style=styles.MAGENTA, show=False, end=''),
        'is handled like a normal call to',
        cprint("print()", style=styles.MAGENTA, show=False, end=''))
    cprint('\t\t\t- ',
        cprint('print', style=styles.CYAN, show=False, end=''),
        '("this is a number:", 4)', sep='')
    cprint('\t\t\t- ',
        cprint('cprint', style=styles.CYAN, show=False, end=''),
        '("this is a number:", 4)', sep='')
    cprint('\t\t\t\t- these statements are equivalent')
    # adding a style
    cprint('\t\t- you can a style like this:')
    cprint('\t\t\t- ',
        cprint('cprint', style=styles.CYAN, show=False, end=''),
        '("some green text", style=styles.GREEN)', sep='')
    cprint("\t\t\t\tsome green text", style=styles.GREEN)
    # adding multiple styles
    cprint('\t\t- you can multiple styles like this:')
    cprint('\t\t\t- ',
        cprint('cprint', style=styles.CYAN, show=False, end=''),
        '("some text", style=[styles.YELLOW, styles.UNDERLINE])',
        sep='')
    cprint("\t\t\t\tsome text",
        style=[styles.YELLOW, styles.UNDERLINE])

# functions the same as the default print function, but with a style parameter and
# some other custom options
def cprint(*args, style='', sep=' ', end='\n', file=sys.stdout, flush=False,
        reset=True, remove_old_styles=True, override_defaults=False, show=True):
    ret = ''
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
        if show:
            print(styles.DONE, end='', sep=sep, file=file, flush=flush)
        ret += styles.DONE
    # start new style(s)
    if type(style) == list or type(style) == tuple:
        if show:
            print(''.join([get_style(s) for s in style]),
                end='', sep=sep, file=file, flush=flush)
        ret += ''.join([get_style(s) for s in style])
    else:
        if show:
            print(get_style(style), end='')
        ret += get_style(style)
    # print output
    if reset:
        if show:
            print(*args, sep=sep, end='', file=file, flush=flush)
            print(styles.DONE, end=end)
        ret += sep.join([str(a) for a in args]) + styles.DONE + end
    else:
        if show:
            print(*args, sep=sep, end=end, file=file, flush=flush)
        ret += sep.join([str(a) for a in args]) + end
    return ret

# test script
if __name__ == '__main__':
    help()
    exit()
    cprint('This is a magenta four:', 4, end='', reset=False, style=styles.MAGENTA)
    cprint(' and this is green', '(this too)\n', style=styles.GREEN)

    set_defaults(reset=False)
    cprint('something in cyan', style=styles.CYAN)
    print('\tStill Cyan!\n')

    cprint('will this reset?', reset=True, style=styles.YELLOW)
    print('\tNope! Reset your defaults!\n')

    cprint('underlined text', reset=True, override_defaults=True,
        style=styles.UNDERLINE)
    print('Not underlined any more, despite default settings\n')

    remove_defaults()
    cprint('red AND underline?!', style=[styles.RED, styles.UNDERLINE])
    print('No style any more\n')

    cprint('cyan background\n', style=styles.CYAN_BG)

    cprint("LOTS OF STYLES!\n",
        style=[styles.RED_BG, styles.YELLOW, styles.UNDERLINE])