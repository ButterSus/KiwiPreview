from __future__ import annotations

# IMPORTS
# =======>

# noinspection PyUnresolvedReferences
import typing
import tokenize
from enum import IntEnum

# EXPORTS
# =======>

__all__ = [
    'TokenType'
]


# MAIN CONTENT
# ============>

class TokenType(IntEnum):
    """
    The token types. This is a wrapper around the tokenize module.

    Attributes
    ----------
    AMPER : int
        The ampersand token. (i.e. &)
    AMPEREQUAL : int
        The ampersand equal token. (i.e. &=)
    AT : int
        The at token. (i.e. @)
    ATEQUAL : int
        The at equal token. (i.e. @=)
    CIRCUMFLEX : int
        The circumflex token. (i.e. ^)
    CIRCUMFLEXEQUAL : int
        The circumflex equal token. (i.e. ^=)
    COLON : int
        The colon token. (i.e. :)
    COMMA : int
        The comma token. (i.e. ,)
    COMMENT : int
        The comment token. (i.e. #)
    UNFINISHED : int
        The dedent token. (i.e. dedent)
    DOT : int
        The dot token. (i.e. .)
    DOUBLESLASH : int
        The double slash token. (i.e. //)
    DOUBLESLASHEQUAL : int
        The double slash equal token. (i.e. //=)
    DOUBLESTAR : int
        The double star token. (i.e. **)
    DOUBLESTAREQUAL : int
        The double star equal token. (i.e. **=)
    ELLIPSIS : int
        The ellipsis token. (i.e. ...)
    ENCODING : int
        The encoding token. (i.e. encoding)
    ENDMARKER : int
        The end marker token. (i.e. endmarker)
    EQEQUAL : int
        The equal equal token. (i.e. ==)
    EQUAL : int
        The equal token. (i.e. =)
    ERRORTOKEN : int
        The error token. (i.e. errortoken)
    GREATER : int
        The greater token. (i.e. >)
    GREATEREQUAL : int
        The greater equal token. (i.e. >=)
    CNAME : int
        The indent token. (i.e. indent)
    LBRACE : int
        The left brace token. (i.e. {)
    LEFTSHIFT : int
        The left shift token. (i.e. <<)
    LEFTSHIFTEQUAL : int
        The left shift equal token. (i.e. <<=)
    LESS : int
        The less token. (i.e. <)
    LESSEQUAL : int
        The less equal token. (i.e. <=)
    LPAR : int
        The left parenthesis token. (i.e. ()
    LSQB : int
        The left square bracket token. (i.e. [)
    MINEQUAL : int
        The minus equal token. (i.e. -=)
    MINUS : int
        The minus token. (i.e. -)
    NAME : int
        The name token. (i.e. name)
    NEWLINE : int
        The new line token. (i.e. newline)
    NL : int
        The new line token. (i.e. nl)
    NOTEQUAL : int
        The not equal token. (i.e. !=)
    NT_OFFSET : int
        The nt offset token. (i.e. nt_offset)
    NUMBER : int
        The number token. (i.e. number)
    N_TOKENS : int
        The n tokens token. (i.e. n_tokens)
    OP : int
        The op token. (i.e. op)
    PERCENT : int
        The percent token. (i.e. %)
    PERCENTEQUAL : int
        The percent equal token. (i.e. %=)
    PLUS : int
        The plus token. (i.e. +)
    PLUSEQUAL : int
        The plus equal token. (i.e. +=)
    RARROW : int
        The right arrow token. (i.e. ->)
    RBRACE : int
        The right brace token. (i.e. })
    RIGHTSHIFT : int
        The right shift token. (i.e. >>)
    RIGHTSHIFTEQUAL : int
        The right shift equal token. (i.e. >>=)
    RPAR : int
        The right parenthesis token. (i.e. ))
    RSQB : int
        The right square bracket token. (i.e. ])
    SEMI : int
        The semicolon token. (i.e. ;)
    SLASH : int
        The slash token. (i.e. /)
    SLASHEQUAL : int
        The slash equal token. (i.e. /=)
    STAR : int
        The star token. (i.e. *)
    STAREQUAL : int
        The star equal token. (i.e. *=)
    STRING : int
        The string token. (i.e. string)
    TILDE : int
        The tilde token. (i.e. ~)
    VBAR : int
        The vbar token. (i.e. |)
    VBAREQUAL : int
        The vbar equal token. (i.e. |=)

    Notes
    -----
    It's used by the lexer to identify the token type and print it out.
    """
    AMPER = tokenize.AMPER
    AMPEREQUAL = tokenize.AMPEREQUAL
    AT = tokenize.AT
    ATEQUAL = tokenize.ATEQUAL
    CIRCUMFLEX = tokenize.CIRCUMFLEX
    CIRCUMFLEXEQUAL = tokenize.CIRCUMFLEXEQUAL
    COLON = tokenize.COLON
    COMMA = tokenize.COMMA
    COMMENT = tokenize.COMMENT
    UNFINISHED = tokenize.DEDENT  # UNFINISHED is custom token type, its' purpose is to mark unfinished nodes.
    DOT = tokenize.DOT
    DOUBLESLASH = tokenize.DOUBLESLASH
    DOUBLESLASHEQUAL = tokenize.DOUBLESLASHEQUAL
    DOUBLESTAR = tokenize.DOUBLESTAR
    DOUBLESTAREQUAL = tokenize.DOUBLESTAREQUAL
    ELLIPSIS = tokenize.ELLIPSIS
    ENCODING = tokenize.ENCODING
    ENDMARKER = tokenize.ENDMARKER
    EQEQUAL = tokenize.EQEQUAL
    EQUAL = tokenize.EQUAL
    ERRORTOKEN = tokenize.ERRORTOKEN
    GREATER = tokenize.GREATER
    GREATEREQUAL = tokenize.GREATEREQUAL
    CNAME = tokenize.INDENT  # CNAME is custom token type, it's not in the tokenize module.
    LBRACE = tokenize.LBRACE
    LEFTSHIFT = tokenize.LEFTSHIFT
    LEFTSHIFTEQUAL = tokenize.LEFTSHIFTEQUAL
    LESS = tokenize.LESS
    LESSEQUAL = tokenize.LESSEQUAL
    LPAR = tokenize.LPAR
    LSQB = tokenize.LSQB
    MINEQUAL = tokenize.MINEQUAL
    MINUS = tokenize.MINUS
    NAME = tokenize.NAME
    NEWLINE = tokenize.NEWLINE
    NL = tokenize.NL
    NOTEQUAL = tokenize.NOTEQUAL
    NT_OFFSET = tokenize.NT_OFFSET
    NUMBER = tokenize.NUMBER
    N_TOKENS = tokenize.N_TOKENS
    OP = tokenize.OP
    PERCENT = tokenize.PERCENT
    PERCENTEQUAL = tokenize.PERCENTEQUAL
    PLUS = tokenize.PLUS
    PLUSEQUAL = tokenize.PLUSEQUAL
    RARROW = tokenize.RARROW
    RBRACE = tokenize.RBRACE
    RIGHTSHIFT = tokenize.RIGHTSHIFT
    RIGHTSHIFTEQUAL = tokenize.RIGHTSHIFTEQUAL
    RPAR = tokenize.RPAR
    RSQB = tokenize.RSQB
    SEMI = tokenize.SEMI
    SLASH = tokenize.SLASH
    SLASHEQUAL = tokenize.SLASHEQUAL
    STAR = tokenize.STAR
    STAREQUAL = tokenize.STAREQUAL
    STRING = tokenize.STRING
    TILDE = tokenize.TILDE
    VBAR = tokenize.VBAR
    VBAREQUAL = tokenize.VBAREQUAL

    @property
    def name(self) -> str:
        """
        Returns the name of the token type.

        Returns
        -------
        str
            The name of the token type.

        Doctests
        --------
        1. Get the name of the token type.
        >>> from frontend.lexer.TokenType import *
        >>> import tokenize
        >>> TokenType.NUMBER.name
        'NUMBER'

        2. Get the name of the token type using the tokenize module.
        >>> TokenType(tokenize.NUMBER).name
        'NUMBER'

        3. Check if enum is int.
        >>> TokenType.NUMBER + 5 == tokenize.NUMBER + 5
        True
        """
        return self._name_
