"""
Lexer package.

This package contains the lexer for the frontend.

Classes
-------
Lexer
    The lexer class for the frontend.
TokenInfo
    A class that represents a token.
TokenType
    An enumeration of all the token types.

Notes
-----
The lexer is a wrapper around the tokenize module, mainly for convenience.
Also it's worth noting that the line and column numbers are 1-indexed.
"""

from .Lexer import Lexer
from .TokenInfo import TokenInfo
from .TokenType import TokenType
