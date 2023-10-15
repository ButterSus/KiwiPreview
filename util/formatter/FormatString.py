from __future__ import annotations

# IMPORTS
# =======>

# noinspection PyUnresolvedReferences
import typing
from util.formatter.TextColor import *
from util.formatter.TextEffects import *
from dataclasses import dataclass, field
from copy import deepcopy

# EXPORTS
# =======>

__all__ = [
    'FormatString'
]


# MAIN CONTENT
# ============>

@dataclass
class FormatString:
    """
    A class that represents a format string.

    Attributes
    ----------
    string: typing.Any
        The string.
    color: TextColor
        The color.
    bold: bool
        Whether the string is bold.
    underline: bool
        Whether the string is underlined.
    italic: bool
        Whether the string is italicized.
    strikethrough: bool
        Whether the string is strikethrough.
    minlength: int or None
        The minimum length of the string.
    maxlength: int or None
        The maximum length of the string.

    Notes
    -----
    Color is an BASH escape sequence.

    References
    ----------
    [1] https://misc.flogisoft.com/bash/tip_colors_and_formatting
    """
    string: typing.Any = field(default='')
    color: TextColor | typing.Iterable[TextColor] = field(default=TextColor.RESET)
    bold: bool = field(default=False)
    underline: bool = field(default=False)
    italic: bool = field(default=False)
    strikethrough: bool = field(default=False)
    minlength: typing.Optional[int] = field(default=None)
    maxlength: typing.Optional[int] = field(default=None)

    _strings: typing.List[str] = field(init=False)
    _colors: typing.List[TextColor] = field(init=False)
    _bolds: typing.List[bool] = field(init=False)
    _underlines: typing.List[bool] = field(init=False)
    _italics: typing.List[bool] = field(init=False)
    _strikethroughs: typing.List[bool] = field(init=False)

    def __post_init__(self):
        """
        Initializes the format string.
        """
        self.string = str(self.string)
        self.string = self.string.ljust(self.minlength) if self.minlength is not None else self.string
        self.string = self.string[:self.maxlength - 1] + '…' \
            if self.maxlength is not None and len(self.string) > self.maxlength else self.string
        self._strings = []
        self._colors = []
        self._bolds = []
        self._underlines = []
        self._italics = []
        self._strikethroughs = []
        self._strings.append(self.string)
        self._colors.append(self.color)
        self._bolds.append(self.bold)
        self._underlines.append(self.underline)
        self._italics.append(self.italic)
        self._strikethroughs.append(self.strikethrough)

    def __str__(self) -> str:
        """
        Returns the string representation of the format string.

        Returns
        -------
        str
            The string representation of the format string.
        """
        string = ''
        for i in range(len(self._strings)):
            if isinstance(self._colors[i], TextColor):
                string += self._colors[i].value
            else:
                string += ''.join(map(lambda x: x.value, self._colors[i]))
            if self._bolds[i]:
                string += TextEffects.BOLD.value
            if self._underlines[i]:
                string += TextEffects.UNDERLINE.value
            if self._italics[i]:
                string += TextEffects.ITALIC.value
            if self._strikethroughs[i]:
                string += TextEffects.STRIKETHROUGH.value
            string += self._strings[i] + TextColor.RESET.value
        return string

    def __repr__(self) -> str:
        """
        Returns the string representation of the format string.

        Returns
        -------
        str
            The string representation of the format string.
        """
        return self.__str__()

    def indent(self, indent=4) -> FormatString:
        """
        Indents the format string.

        Parameters
        ----------
        indent: int
            The number of spaces to indent by.

        Returns
        -------
        FormatString
            The indented format string.
        """
        buffer = FormatString(' ' * indent)
        for index, string in enumerate(self._strings):
            lines = list(map(lambda x: FormatString(
                string=x, color=self._colors[index], bold=self._bolds[index], underline=self._underlines[index],
                italic=self._italics[index], strikethrough=self._strikethroughs[index]
            ), string.split('\n')))
            buffer += lines[0]
            for line in lines[1:]:
                buffer += FormatString('\n' + ' ' * indent) + line
        return buffer

    def join(self, strings: typing.Iterable[FormatString | str]) -> FormatString:
        """
        Joins the format strings.

        Parameters
        ----------
        strings: typing.List[FormatString]
            The format strings to join.

        Returns
        -------
        FormatString
            The joined format string.
        """
        buffer = FormatString()
        for index, string in enumerate(strings):
            if index > 0:
                buffer += self
            buffer += string
        return buffer

    def __add__(self, other: FormatString | str) -> FormatString:
        """
        Returns the concatenation of the format strings.

        Parameters
        ----------
        other: FormatString
            The other format string.

        Returns
        -------
        FormatString
            The concatenation of the format strings.
        """
        cself = deepcopy(self)
        other = deepcopy(other)
        if isinstance(other, str):
            other = FormatString(other)
        cself._strings += other._strings
        cself._colors += other._colors
        cself._bolds += other._bolds
        cself._underlines += other._underlines
        cself._italics += other._italics
        cself._strikethroughs += other._strikethroughs
        return cself

    def toRawString(self) -> str:
        """
        Returns the raw string representation of the format string.

        Returns
        -------
        str
            String without any formatting, but with all BASH escape sequences.

        Examples
        --------
        >>> print(FormatString('foo', TextColor.RED).toRawString())
        \033[31mfoo\033[0m

        Notes
        -----
        This method is used for testing.
        """
        string = self.__str__()
        for color, code in TextColor.RawCodes().items():
            string = string.replace(color.value, code)
        for effect, code in TextEffects.RawCodes().items():
            string = string.replace(effect.value, code)
        return string
