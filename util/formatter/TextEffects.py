from __future__ import annotations

# IMPORTS
# =======>

# noinspection PyUnresolvedReferences
import typing
import enum

# EXPORTS
# =======>

__all__ = [
    'TextEffects'
]


# MAIN CONTENT
# ============>

class TextEffects(str, enum.Enum):
    """
    A class that represents text effects.

    Notes
    -----
    Effects are BASH escape sequences.

    References
    ----------
    [1] https://misc.flogisoft.com/bash/tip_colors_and_formatting
    """

    # Effects
    RESET: TextEffects = '\033[0m'
    BOLD: TextEffects = '\033[1m'
    UNDERLINE: TextEffects = '\033[4m'
    ITALIC: TextEffects = '\033[3m'
    STRIKETHROUGH: TextEffects = '\033[9m'

    @classmethod
    def RawCodes(cls) -> typing.Dict[TextEffects, str]:
        return {
            cls.RESET: '\\033[0m',
            cls.BOLD: '\\033[1m',
            cls.UNDERLINE: '\\033[4m',
            cls.ITALIC: '\\033[3m',
            cls.STRIKETHROUGH: '\\033[9m'
        }
