from __future__ import annotations

# IMPORTS
# =======>

# noinspection PyUnresolvedReferences
import typing
import tokenize
import io

# EXPORTS
# =======>

__all__ = [
    'Lexer'
]

# MAIN CONTENT
# ============>

UNPARSABLE_TOKENS: typing.Set[int] = {
    tokenize.ENCODING,
    tokenize.NL,
    tokenize.COMMENT,
    tokenize.INDENT,
    tokenize.DEDENT,
}


class Lexer:
    """
    Lexer class for the frontend.
    """
    source: str
    tokens: typing.Iterable[tokenize.TokenInfo]

    def load(self, source: str) -> Lexer:
        self.source = source
        self.tokens = tokenize.tokenize(
            io.BytesIO(source.encode('utf-8')).readline
        )
        return self

    def _wrapper(self) -> typing.Iterable[tokenize.TokenInfo]:
        for token in self.tokens:
            if token.type in UNPARSABLE_TOKENS:
                continue
            yield token
