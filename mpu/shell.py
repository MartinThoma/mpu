#!/usr/bin/env python

"""Enhancing printed terminal output."""


class Codes:
    """Escape sequences for enhanced shell output."""

    RESET_ALL = "\033[0m"

    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINED = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"

    RESET_BOLD = "\033[21m"
    RESET_DIM = "\033[22m"
    RESET_UNDERLINED = "\033[24m"
    RESET_BLINK = "\033[25m"
    RESET_REVERSE = "\033[27m"
    RESET_HIDDEN = "\033[28m"

    DEFAULT = "\033[39m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    LIGHT_GRAY = "\033[37m"
    DARK_GRAY = "\033[90m"
    LIGHT_RED = "\033[91m"
    LIGHT_GREEN = "\033[92m"
    LIGHT_YELLOW = "\033[93m"
    LIGHT_BLUE = "\033[94m"
    LIGHT_MAGENTA = "\033[95m"
    LIGHT_CYAN = "\033[96m"
    WHITE = "\033[97m"

    BACKGROUND_DEFAULT = "\033[49m"
    BACKGROUND_BLACK = "\033[40m"
    BACKGROUND_RED = "\033[41m"
    BACKGROUND_GREEN = "\033[42m"
    BACKGROUND_YELLOW = "\033[43m"
    BACKGROUND_BLUE = "\033[44m"
    BACKGROUND_MAGENTA = "\033[45m"
    BACKGROUND_CYAN = "\033[46m"
    BACKGROUND_LIGHT_GRAY = "\033[47m"
    BACKGROUND_DARK_GRAY = "\033[100m"
    BACKGROUND_LIGHT_RED = "\033[101m"
    BACKGROUND_LIGHT_GREEN = "\033[102m"
    BACKGROUND_LIGHT_YELLOW = "\033[103m"
    BACKGROUND_LIGHT_BLUE = "\033[104m"
    BACKGROUND_LIGHT_MAGENTA = "\033[105m"
    BACKGROUND_LIGHT_CYAN = "\033[106m"
    BACKGROUND_WHITE = "\033[107m"


def print_table(table):
    """
    Print as a table.

    I recommend looking at [`tabulate`](https://pypi.org/project/tabulate/).

    Parameters
    ----------
    table : list

    Examples
    --------
    >>> print_table([[1, 2, 3], [41, 0, 1]])
     1  2  3
    41  0  1
    """
    table = [[str(cell) for cell in row] for row in table]
    column_widths = [len(cell) for cell in table[0]]
    for row in table:
        for x, cell in enumerate(row):
            column_widths[x] = max(column_widths[x], len(cell))

    formatters = []
    for width in column_widths:
        formatters.append("{:>" + str(width) + "}")
    formatter = "  ".join(formatters)
    for row in table:
        print(formatter.format(*row))


def text_input(text):
    """
    Ask the user for textual input.

    Parameters
    ----------
    text : str
        What the user sees.

    Returns
    -------
    inputed_text : str
        What the user wrote.
    """
    return input(text)
