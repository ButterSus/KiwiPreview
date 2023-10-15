from __future__ import annotations

# IMPORTS
# =======>

# noinspection PyUnresolvedReferences
import typing
from dataclasses import dataclass, field
from abc import ABC
from frontend.lexer import *
from frontend.parser.NodeMeta import *

# EXPORTS
# =======>

__all__ = [
    'Node',
    'File',
    'TokenWrapper',
]


# MAIN CONTENT
# ============>

@dataclass(kw_only=True)
class Node(ABC, metaclass=NodeMeta, is_base=True):
    """
    A class that represents a node in the AST.

    Attributes
    ----------
    name: str
        The name of the node.
    row: int
        The line number of the node.
    column: int
        The column number of the node.
    end_row: int
        The end line number of the node.
    end_column: int
        The end column number of the node.

    Notes
    -----
    The line and column numbers are 1-indexed.

    Doctests
    --------
    >>> Node()
    Node(name='Node', line=None, column=None, end_line=None, end_column=None)
    """

    # We defined field values here so IDEs can autocomplete them
    # But they will be overridden by the metaclass
    name: str = field(default='Node', init=False, repr=True, compare=True)
    row: int = field(default=None)  # will be set by post_init
    column: int = field(default=None)  # will be set by post_init
    end_row: int = field(default=None)  # will be set by post_init
    end_column: int = field(default=None)  # will be set by post_init

    def toFormatString(self, *, indent: int = 4) -> str:
        pass


@dataclass(kw_only=True)
class File(Node, metaclass=NodeMeta, base=Node):
    packageHeader: PackageHeader


@dataclass(kw_only=True)
class PackageHeader(Node, metaclass=NodeMeta, base=Node):
    identifier: Identifier


@dataclass(kw_only=True)
class Identifier(Node, metaclass=NodeMeta, base=Node):
    attrs: typing.List[TokenWrapper]


@dataclass(kw_only=True)
class TokenWrapper(Node, metaclass=NodeMeta, base=Node, no_track=True):
    """
    A node that wraps a token.

    Attributes
    ----------
    token: TokenInfo
        The token to wrap.
    value: str
        The value of the token.
    type: TokenType
        The type of the token.
    """

    token: TokenInfo
    value: str = field(default=None)
    type: TokenType = field(default=None)

    def __post_init__(self):
        self.value = self.value or self.token.value
        self.type = self.type or self.token.type
        self.row = self.token.row
        self.column = self.token.column
        self.end_row = self.token.end_row
        self.end_column = self.token.end_column
