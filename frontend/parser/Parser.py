from __future__ import annotations

import tokenize

# IMPORTS
# =======>

# noinspection PyUnresolvedReferences
from typing import Optional, Any
from pegen.parser import Parser, memoize, memoize_left_rec
import frontend.parser.AST as AST

# EXPORTS
# =======>

__all__ = ["Parser"]


# MAIN CONTENT
# ============>
# Keywords and soft keywords are listed at the end of the parser definition.
class Parser(Parser):
    @memoize
    def start(self) -> Optional[AST.File]:
        # start: packageHeader NEWLINE? $
        mark = self._mark()
        if (
            (i1 := self.packageHeader())
            and (self.expect("NEWLINE"),)
            and (self.expect("ENDMARKER"))
        ):
            return AST.File(packageHeader=i1)
        self._reset(mark)
        return None

    @memoize
    def packageHeader(self) -> Optional[AST.PackageHeader]:
        # packageHeader: 'package' identifier
        mark = self._mark()
        if (self.expect("package")) and (i1 := self.identifier()):
            return AST.PackageHeader(identifier=i1)
        self._reset(mark)
        return None

    @memoize
    def identifier(self) -> Optional[AST.Identifier]:
        # identifier: '.'.simpleIdentifier+
        mark = self._mark()
        if i1 := self._gather_1():
            return AST.Identifier(attrs=i1)
        self._reset(mark)
        return None

    @memoize
    def simpleIdentifier(self) -> Optional[AST.TokenWrapper]:
        # simpleIdentifier: NAME
        mark = self._mark()
        if i1 := self.name():
            return AST.TokenWrapper(token=i1)
        self._reset(mark)
        return None

    @memoize
    def importList(self) -> Optional[Any]:
        # importList: DEDENT
        mark = self._mark()
        if _dedent := self.expect("DEDENT"):
            return _dedent
        self._reset(mark)
        return None

    @memoize
    def topLevelObject(self) -> Optional[Any]:
        # topLevelObject: DEDENT
        mark = self._mark()
        if _dedent := self.expect("DEDENT"):
            return _dedent
        self._reset(mark)
        return None

    @memoize
    def _loop0_2(self) -> Optional[Any]:
        # _loop0_2: '.' simpleIdentifier
        mark = self._mark()
        children = []
        while (self.expect(".")) and (elem := self.simpleIdentifier()):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_1(self) -> Optional[Any]:
        # _gather_1: simpleIdentifier _loop0_2
        mark = self._mark()
        if (elem := self.simpleIdentifier()) is not None and (
            seq := self._loop0_2()
        ) is not None:
            return [elem] + seq
        self._reset(mark)
        return None

    KEYWORDS = ("package",)
    SOFT_KEYWORDS = ()
