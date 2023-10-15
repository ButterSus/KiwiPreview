from __future__ import annotations

# IMPORTS
# =======>

# noinspection PyUnresolvedReferences
import typing
import enum

# EXPORTS
# =======>

__all__ = [
    'TextColor'
]


# MAIN CONTENT
# ============>


class TextColor(str, enum.Enum):
    """
    A class that represents a color.

    Notes
    -----
    Color is an BASH escape sequence.
    Background colors are separated by BG_.

    References
    ----------
    [1] https://misc.flogisoft.com/bash/tip_colors_and_formatting
    """
    # Main colors
    RESET: TextColor = '\033[0m'
    BLACK: TextColor = '\033[30m'
    RED: TextColor = '\033[31m'
    GREEN: TextColor = '\033[32m'
    YELLOW: TextColor = '\033[33m'
    BLUE: TextColor = '\033[34m'
    PURPLE: TextColor = '\033[35m'
    CYAN: TextColor = '\033[36m'
    LIGHT_GRAY: TextColor = '\033[37m'

    # Bright colors
    DARK_GRAY: TextColor = '\033[90m'
    LIGHT_RED: TextColor = '\033[91m'
    LIGHT_GREEN: TextColor = '\033[92m'
    LIGHT_YELLOW: TextColor = '\033[93m'
    LIGHT_BLUE: TextColor = '\033[94m'
    LIGHT_PURPLE: TextColor = '\033[95m'
    LIGHT_CYAN: TextColor = '\033[96m'
    WHITE: TextColor = '\033[97m'

    # Background colors
    BG_BLACK: TextColor = '\033[40m'
    BG_RED: TextColor = '\033[41m'
    BG_GREEN: TextColor = '\033[42m'
    BG_YELLOW: TextColor = '\033[43m'
    BG_BLUE: TextColor = '\033[44m'
    BG_PURPLE: TextColor = '\033[45m'
    BG_CYAN: TextColor = '\033[46m'
    BG_LIGHT_GRAY: TextColor = '\033[47m'

    # Bright background colors
    BG_DARK_GRAY: TextColor = '\033[100m'
    BG_LIGHT_RED: TextColor = '\033[101m'
    BG_LIGHT_GREEN: TextColor = '\033[102m'
    BG_LIGHT_YELLOW: TextColor = '\033[103m'
    BG_LIGHT_BLUE: TextColor = '\033[104m'
    BG_LIGHT_PURPLE: TextColor = '\033[105m'
    BG_LIGHT_CYAN: TextColor = '\033[106m'
    BG_WHITE: TextColor = '\033[107m'

    @classmethod
    def RawCodes(cls) -> typing.Dict[TextColor, str]:
        return {
            cls.RESET: '\\033[0m',
            cls.BLACK: '\\033[30m',
            cls.RED: '\\033[31m',
            cls.GREEN: '\\033[32m',
            cls.YELLOW: '\\033[33m',
            cls.BLUE: '\\033[34m',
            cls.PURPLE: '\\033[35m',
            cls.CYAN: '\\033[36m',
            cls.LIGHT_GRAY: '\\033[37m',
            cls.DARK_GRAY: '\\033[90m',
            cls.LIGHT_RED: '\\033[91m',
            cls.LIGHT_GREEN: '\\033[92m',
            cls.LIGHT_YELLOW: '\\033[93m',
            cls.LIGHT_BLUE: '\\033[94m',
            cls.LIGHT_PURPLE: '\\033[95m',
            cls.LIGHT_CYAN: '\\033[96m',
            cls.WHITE: '\\033[97m',
            cls.BG_BLACK: '\\033[40m',
            cls.BG_RED: '\\033[41m',
            cls.BG_GREEN: '\\033[42m',
            cls.BG_YELLOW: '\\033[43m',
            cls.BG_BLUE: '\\033[44m',
            cls.BG_PURPLE: '\\033[45m',
            cls.BG_CYAN: '\\033[46m',
            cls.BG_LIGHT_GRAY: '\\033[47m',
            cls.BG_DARK_GRAY: '\\033[100m',
            cls.BG_LIGHT_RED: '\\033[101m',
            cls.BG_LIGHT_GREEN: '\\033[102m',
            cls.BG_LIGHT_YELLOW: '\\033[103m',
            cls.BG_LIGHT_BLUE: '\\033[104m',
            cls.BG_LIGHT_PURPLE: '\\033[105m',
            cls.BG_LIGHT_CYAN: '\\033[106m',
            cls.BG_WHITE: '\\033[107m',
        }
