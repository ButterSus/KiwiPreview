from __future__ import annotations

# IMPORTS
# =======>

# noinspection PyUnresolvedReferences
import typing
import tokenize
from frontend.lexer.TokenType import *
from util.formatter import *

# EXPORTS
# =======>

__all__ = [
    'TokenInfo'
]


# MAIN CONTENT
# ============>

class TokenInfo(tokenize.TokenInfo):
    # noinspection PyUnresolvedReferences
    """
    A wrapper around tokenize.TokenInfo that adds some useful properties and methods

    Attributes
    ----------
    type: TokenType
        The type of the token
    value: str
        The value of the token
    row: int
        The line number of the token
    column: int
        The column number of the token
    end_row: int
        The end line number of the token
    end_column: int
        The end column number of the token

    Notes
    -----
    The line and column numbers are 1-indexed.
    """
    type: TokenType

    @property
    def value(self) -> str:
        return self.string

    @property
    def row(self) -> int:
        return self.start[0]

    @property
    def column(self) -> int:
        return self.start[1]

    @property
    def end_row(self) -> int:
        return self.end[0]

    @property
    def end_column(self) -> int:
        return self.end[1]

    def __new__(cls, token: tokenize.TokenInfo):
        return super().__new__(cls, TokenType(token.exact_type), *token[1:])  # type: ignore

    def toFormatString(self) -> FormatString:
        """
        Returns pretty formatted string of the token

        Returns
        -------
        FormatString
            The formatted string
        """
        return FormatString(
            string=f'''{FormatString(
                string=self.row,
                color=TextColor.YELLOW,
                bold=True,
                minlength=2,
            )} | {FormatString(
                string=self.column,
                color=TextColor.YELLOW,
                bold=True,
                minlength=2,
            )} | {FormatString(
                string=self.type.name,
                color=TextColor.BLUE,
                bold=True,
                minlength=20,
                maxlength=20,
            )} | {FormatString(
                string=self.value,
                color=TextColor.GREEN,
                bold=True,
            )}'''
        )
