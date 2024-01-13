from __future__ import annotations

# IMPORTS
# =======>

# noinspection PyUnresolvedReferences
import typing
from dataclasses import dataclass, field
from abc import ABC
from frontend.lexer import *
from frontend.parser.NodeMeta import *
from util.formatter import *

# EXPORTS
# =======>

__all__ = [
    'Node',
    'File',
    'TokenWrapper',
    'Identifier',
    'ImportAlias',
    'Null',
    'ImportHeader',
    'PackageHeader',
    'Declaration',
    'FunctionDeclaration',
    'List',
]

# MAIN CONTENT
# ============>

rainbow_colors = [
    TextColor.LIGHT_RED + TextColor.BG_DARK_GRAY,
    TextColor.LIGHT_YELLOW + TextColor.BG_DARK_GRAY,
    TextColor.LIGHT_GREEN + TextColor.BG_DARK_GRAY,
    TextColor.LIGHT_CYAN + TextColor.BG_DARK_GRAY,
    TextColor.LIGHT_BLUE + TextColor.BG_DARK_GRAY,
    TextColor.LIGHT_PURPLE + TextColor.BG_DARK_GRAY,
]

rainbow_list_index = -1


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
    children: typing.List[Node | typing.List | typing.Any]
        The children of the node.

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
    name: str = field(default=None, init=False, repr=True, compare=True)
    row: int = field(default=None)
    column: int = field(default=None)
    end_row: int = field(default=None)
    end_column: int = field(default=None)
    children: typing.List[str] = field(default=None, init=False, repr=False, compare=False)

    def toFormatString(self, *, indent: int = 4) -> FormatString:
        """
        Converts the node to a formatted string.

        Parameters
        ----------
        indent: int
            The number of spaces to indent by.

        Returns
        -------
        FormatString
            The formatted string.
        """
        if len(self.children) == 0:
            return FormatString(
                string=f"<{self.name}>",
                bold=True,
                color=TextColor.BLUE,
            )
        global rainbow_list_index
        rainbow_list_index = (rainbow_list_index + 1) % len(rainbow_colors)
        result = FormatString(
            string=f"<{self.name}>",
            bold=True,
            color=TextColor.BLUE,
        ) + ' ' + FormatString('{', color=rainbow_colors[rainbow_list_index]) + '\n' + FormatString("\n").join([
            FormatString(child, color=TextColor.LIGHT_YELLOW) + ': ' + FormatString(
                self.__getattribute__(child).toFormatString(indent=indent)
            ) for child in self.children
        ]).indent(indent) + '\n' + FormatString('}', color=rainbow_colors[rainbow_list_index])
        rainbow_list_index = (rainbow_list_index - 1) % len(rainbow_colors)
        return result


@dataclass(kw_only=True)
class List(Node, list, metaclass=NodeMeta, is_base=True):
    """
    A class that represents a list of nodes in the AST.

    Attributes
    ----------
    elements: typing.List[Node]
        The elements of the list.

    Notes
    -----
    You should use this class instead of the built-in list class.
    This is because this class has some extra features that are necessary for the parser.
    """
    name: str = field(default='List', init=False, repr=True, compare=True)
    children: typing.List[str] = field(default_factory=list, init=False, repr=False, compare=False)
    elements: typing.List[Node] = field(default_factory=list)

    def __post_init__(self):
        self.extend(self.elements)
        if len(self) == 0:
            self.row = -1
            self.column = -1
            self.end_row = -1
            self.end_column = -1
            return
        self.row = self[0].row
        self.column = self[0].column
        self.end_row = self[-1].end_row
        self.end_column = self[-1].end_column

    def toFormatString(self, *, indent: int = 4) -> FormatString:
        global rainbow_list_index
        rainbow_list_index = (rainbow_list_index + 1) % len(rainbow_colors)
        content = FormatString(FormatString("[", color=rainbow_colors[rainbow_list_index]) + (
            "\n" if len(self.elements) > 0 else str())) + FormatString(",\n").join(
            [FormatString(f" {index}.", color=TextColor.LIGHT_GREEN + TextColor.BG_BLACK) + ' ' +
             element.toFormatString(indent=indent) for index, element in enumerate(self, start=1)
             ]).indent(indent) + ("\n" if len(self.elements) > 0 else str()) + FormatString(
            "]", color=rainbow_colors[rainbow_list_index])
        rainbow_list_index = (rainbow_list_index - 1) % len(rainbow_colors)
        return FormatString(
            string=f" L:",
            bold=True,
            color=TextColor.BLUE + TextColor.BG_BLACK
        ) + FormatString(
            string=f"{len(self)} ",
            color=TextColor.RED + TextColor.BG_BLACK,
        ) + ' ' + content

    def __bool__(self):
        return True

    def __add__(self, other) -> List:
        if isinstance(other, List):
            return List(elements=self.elements + other.elements)
        return List(elements=self.elements + other)


# late init
# --------->
late_names: typing.Dict[str, typing.Tuple[str]] = dict()


def late_init(name: str, *typeNames: str):
    """
    Late init a node type.

    Parameters
    ----------
    name: str
        The name of the node type.
    typeNames: typing.Tuple[str]
        The names of the types to late init.
    """
    late_names[name] = typeNames


# main.gram
# --------->
@dataclass(kw_only=True)
class File(Node, metaclass=NodeMeta, base=Node):
    packageHeader: PackageHeader
    importList: List[ImportHeader]
    declarations: List[Declaration]


# identifier.gram
# --------------->
@dataclass(kw_only=True)
class Identifier(Node, metaclass=NodeMeta, base=Node):
    attrs: List[TokenWrapper]

    def toFormatString(self, *, indent: int = 4) -> FormatString:
        return FormatString(
            string=f"I:",
            color=TextColor.BLUE + TextColor.BG_BLACK,
        ) + FormatString(
            f'"{".".join([attr.value for attr in self.attrs])}"',
            color=TextColor.GREEN + TextColor.BG_BLACK,
        )


late_init('simpleIdentifier', 'TokenWrapper')
simpleIdentifier: typing.Type[TokenWrapper]


# function.gram
@dataclass(kw_only=True)
class FunctionDeclaration(Node, metaclass=NodeMeta, base=Node):
    modifiers: List[TokenWrapper]
    receiverType: UserType | Null
    identifier: Identifier


Declaration = FunctionDeclaration


@dataclass(kw_only=True)
class PackageHeader(Node, metaclass=NodeMeta, base=Node):
    identifier: Identifier


@dataclass(kw_only=True)
class ImportHeader(Node, metaclass=NodeMeta, base=Node):
    identifier: Identifier
    alias: ImportAlias | Null


@dataclass(kw_only=True)
class Null(Node, metaclass=NodeMeta, base=Node, no_track=True):
    row: int = field(default=-1)
    column: int = field(default=-1)
    end_row: int = field(default=-1)
    end_column: int = field(default=-1)

    def toFormatString(self, *, indent: int = 4) -> FormatString:
        return FormatString(
            string=f" NULL ",
            color=TextColor.BLUE + TextColor.BG_BLACK,
        )


@dataclass(kw_only=True)
class ImportAlias(Node, metaclass=NodeMeta, base=Node):
    identifier: TokenWrapper | Null = field(default_factory=Null)

    def toFormatString(self, *, indent: int = 4) -> FormatString:
        if isinstance(self.identifier, Null):
            return FormatString(
                string=f" ALL* ",
                color=TextColor.BLUE + TextColor.BG_BLACK,
            )
        return super().toFormatString(indent=indent)


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

    def toFormatString(self, *args, **kwargs) -> FormatString:
        return FormatString(
            string=f"\"{self.value}\"",
            color=TextColor.GREEN + TextColor.BG_BLACK,
        )


# late init
# --------->
for name, typeNames in late_names.items():
    if len(typeNames) == 1:
        globals()[name] = globals()[typeNames[0]]
    else:
        globals()[name] = typing.Union[tuple(globals()[typeName] for typeName in typeNames)]
