"""
Lexer class for the frontend.

Notes
-----
Lexer *can be rewritten in future releases* to use a different tokenizer, as it
is a wrapper around the tokenize module.

References
----------
[1] https://docs.python.org/3/library/tokenize.html
"""

from __future__ import annotations

# IMPORTS
# =======>

# noinspection PyUnresolvedReferences
import typing
import tokenize
import io
from pegen.tokenizer import Tokenizer
from .TokenType import *
from .TokenInfo import *

# EXPORTS
# =======>

__all__ = [
    'Lexer'
]

# MAIN CONTENT
# ============>

UNPARSABLE_TOKENS: typing.Set[TokenType] = {
    TokenType.ENCODING,
    TokenType.NL,
    TokenType.COMMENT,
    TokenType.CNAME,
    TokenType.UNFINISHED,
    TokenType.ERRORTOKEN,
}


class Lexer:
    """
    Lexer class for the frontend.

    Attributes
    ----------
    source: str
        The source code.
    _tokenStream: typing.Iterator[TokenInfo]
        The token stream.

    Notes
    -----
    This is a wrapper around the tokenize module, mainly for convenience.
    """
    source: str
    _tokenStream: typing.Iterator[tokenize.TokenInfo]

    def load(self, source: str) -> Lexer:
        """
        Loads the source code into the lexer.

        Parameters
        ----------
        source: str
            The source code.

        Returns
        -------
        Lexer
            The lexer.

        Notes
        -----
        This method is chainable. (i.e. it returns the lexer itself to allow for method chaining)
        """
        self.source = source
        self._tokenStream = tokenize.tokenize(
            io.BytesIO(source.encode('utf-8')).readline
        )
        return self

    def wrapper(self) -> typing.Iterator[TokenInfo]:
        """
        Wraps the token stream into a TokenInfo stream.

        Returns
        -------
        typing.Iterable[tokenize.TokenInfo]
            The TokenInfo stream.

        Notes
        -----
        This method is private.
        """
        for token in self._tokenStream:
            if token.type == tokenize.ERRORTOKEN and token.string == '$':
                next_token = next(self._tokenStream)
                if next_token.type != tokenize.NAME or token.end[1] != next_token.start[1]:
                    yield TokenInfo(token)
                    yield TokenInfo(next_token)
                    continue
                yield TokenInfo(tokenize.TokenInfo(
                    type=TokenType.CNAME,
                    string=f'${next_token.string}',
                    start=token.start,
                    end=next_token.end,
                    line=token.line,
                ))  # type: ignore
            if token.type in UNPARSABLE_TOKENS:
                continue
            yield TokenInfo(token)

    def tokenize(self) -> Tokenizer:
        """
        Tokenizes the source code.

        Returns
        -------
        Tokenizer
            The tokenizer.

        Notes
        -----
        This method is mainly used to adapt the tokenizer to the parser.
        """
        return Tokenizer(self.wrapper())
