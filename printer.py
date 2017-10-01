import sys

TEMPLATE = '\033[{}m'
DEFAULTS = None
DONE = '\033[0m'

# available styles
class styles:
    BLACK = '\033[30m'
    black = '\033[30m'
    RED = '\033[91m'
    red = '\033[91m'
    GREEN = '\033[92m'
    green = '\033[92m'
    YELLOW = '\033[93m'
    yellow = '\033[93m'
    BLUE = '\033[34m'
    blue = '\033[34m'
    MAGENTA = '\033[95m'
    magenta = '\033[95m'
    CYAN = '\033[36m'
    cyan = '\033[36m'
    WHITE = '\033[37m'
    white = '\033[37m'

    BLACK_BG = '\033[40m'
    black_bg = '\033[40m'
    RED_BG = '\033[41m'
    red_bg = '\033[41m'
    GREEN_BG = '\033[42m'
    green_bg = '\033[42m'
    YELLOW_BG = '\033[43m'
    yellow_bg = '\033[43m'
    BLUE_BG = '\033[44m'
    blue_bg = '\033[44m'
    MAGENTA_BG = '\033[45m'
    magenta_bg = '\033[45m'
    CYAN_BG = '\033[46m'
    cyan_bg = '\033[46m'
    WHITE_BG = '\033[47m'
    white_bg = '\033[47m'

    BOLD = '\033[1m'
    bold = '\033[1m'
    UNDERLINE = '\033[4m'
    underline = '\033[4m'
    ITALICS = '\033[3m'
    italics = '\033[3m'
    INVERSE = '\033[7m'
    inverse = '\033[7m'

# sets defaults from this point on, until a reset
def set_defaults(sep=None, end=None, file=None, flush=None, reset=None,
        remove_old_styles=None, show=None):
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
    if show != None:
        DEFAULTS['show'] = show

# resets default settings
def remove_defaults():
    global DEFAULTS
    DEFAULTS = None

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
        if 'show' in DEFAULTS:
            show = DEFAULTS[show]

    get_style = lambda x: TEMPLATE.format(x) if type(x) == int else x

    # end old styles
    if remove_old_styles:
        if show:
            print(DONE, end='', sep=sep, file=file, flush=flush)
        ret += DONE
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
            print(DONE, end=end)
        ret += sep.join([str(a) for a in args]) + DONE + end
    else:
        if show:
            print(*args, sep=sep, end=end, file=file, flush=flush)
        ret += sep.join([str(a) for a in args]) + end
    return ret

# returns a string representing a progress bar
def get_bar(current, total, bar_char='-', length=60, precision=2,
        show_progress=True, bookends='[]', prog_format='%', title=''):
    perc = current/total
    bar = ''
    if len(title) > 0:
        bar += title + ' '
    bar += bookends[0] + '{}' + bookends[1]
    if show_progress:
        if prog_format == '/':
            bar += ' {}/{}'.format(current, total)
        else:
            bar += ' {}%'.format(round(perc*100, precision)
                if precision > 0 else int(perc*100))
    num_chars = int(perc*length)
    return bar.format(bar_char*num_chars + ' '*(length - num_chars))

# outputs a progress bar to the screen
def print_bar(current, total, bar_char='-', length=60, precision=2,
        show_progress=True, bookends='[]', prog_format='%', title=''):
    print(get_bar(current, total, bar_char, length, precision,
        show_progress, bookends, prog_format, title))

# prints a usage message
def help():
    # basic overview
    cprint('\nTo print in a certain style:\n', style=styles.INVERSE)
    cprint('\tcprint(style, *args)', style=styles.YELLOW)
    cprint("\t\t- returns a printable string, and (optionally) prints it")
    # similarities with "print()"
    cprint('\t\t-',
        cprint("'args'", style=styles.MAGENTA, show=False, end=''),
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
    cprint('\t\t- you can multiple styles like this (tuple or list):')
    cprint('\t\t\t- ',
        cprint('cprint', style=styles.CYAN, show=False, end=''),
        '("some text", style=[styles.YELLOW, styles.UNDERLINE])',
        sep='')
    cprint("\t\t\t\tsome text",
        style=[styles.YELLOW, styles.UNDERLINE])
    # specify by number
    cprint('\t\t- you can specify ANSI codes by number as well:')
    cprint('\t\t\t- ',
        cprint('cprint', style=styles.CYAN, show=False, end=''),
        '("number 41", style=41)',
        sep='')
    cprint("\t\t\t\tnumber 41", style=41)
    cprint('\t\t\t- ',
        cprint('cprint', style=styles.CYAN, show=False, end=''),
        '("number list", style=[41, styles.GREEN])',
        sep='')
    cprint("\t\t\t\tnumber list", style=[41, styles.GREEN])

    # optional args
    cprint("\n\t\t Optional Arguments", style=styles.MAGENTA)
    cprint("\t\t\t- All optional arguments to print() are supported")
    cprint("\t\t\t- 'style'             : specifies style argument(s)")
    cprint("\t\t\t- 'remove_old_styles' : resets styles before printing")
    cprint("\t\t\t- 'override_defaults' : ignores default settings")
    cprint("\t\t\t- 'show'              : determines if text should print")

    # defaults
    cprint('\nSetting defaults:\n', style=styles.INVERSE)
    cprint('\tset_defaults()', style=styles.YELLOW)
    cprint('\t\t- has same optional values as cprint(), sets values as default')
    cprint('\t\t\t- "override_defaults" not supported')

    cprint('\nRemoving defaults:\n', style=styles.INVERSE)
    cprint('\tremove_defaults()', style=styles.YELLOW)
    cprint('\t\t- removes all custom defaults')
    cprint()

# test script
if __name__ == '__main__':
    # show help
    if '-h' in sys.argv or '--help' in sys.argv:
        help()
        exit()

    # do sample prints
    cprint('This is a magenta four:', 4, end='', reset=False, style=styles.MAGENTA)
    cprint(' and this is green', '(this too)\n', style=styles.GREEN)

    set_defaults(reset=False)
    cprint('something in cyan', style=styles.CYAN)
    print('\tStill cyan!\n')

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

    cprint("Test with number (33)", style=33)