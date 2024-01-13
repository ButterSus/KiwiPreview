from __future__ import annotations

import tokenize

# IMPORTS
# =======>

# noinspection PyUnresolvedReferences
from typing import Optional, Any
from pegen.parser import Parser
from frontend.parser.memoizetools import memoize, memoize_left_rec
import frontend.parser.AST as AST

# EXPORTS
# =======>

__all__ = ["Parser"]


# MAIN CONTENT
# ============>

memoize.List = AST.List
memoize_left_rec.List = AST.List


# noinspection PyRedundantParentheses
# noinspection PyUnboundLocalVariable
# Keywords and soft keywords are listed at the end of the parser definition.
class Parser(Parser):
    @memoize
    def start(self) -> Optional[AST.File]:
        # start: packageHeader importList topLevelObjectList semi? &&($)
        mark = self._mark()
        if (
            (i1 := self.packageHeader())
            and (i2 := self.importList())
            and (i3 := self.topLevelObjectList())
            and (self.semi(),)
            and (self.expect_forced(self.expect("ENDMARKER"), """($)"""))
        ):
            return AST.File(packageHeader=i1, importList=i2, declarations=i3)
        self._reset(mark)
        return None

    @memoize
    def functionDeclaration(self) -> Optional[AST.FunctionDeclaration]:
        # functionDeclaration: modifiers? 'fun' receiverType identifier '(' ')'
        mark = self._mark()
        if (
            (i1 := self.modifiers(),)
            and (self.expect("fun"))
            and (i2 := self.receiverType())
            and (i3 := self.identifier())
            and (self.expect("("))
            and (self.expect(")"))
        ):
            return AST.FunctionDeclaration(modifiers=i1, receiverType=i2, identifier=i3)
        self._reset(mark)
        return None

    @memoize
    def identifier(self) -> Optional[AST.Identifier]:
        # identifier: simpleIdentifier identifier_i2_List
        mark = self._mark()
        if (i1 := self.simpleIdentifier()) and (i2 := self.identifier_i2_List()):
            return AST.Identifier(attrs=AST.List(elements=list([i1])) + i2)
        self._reset(mark)
        return None

    @memoize
    def identifier_i2_List(self) -> Optional[Any]:
        # identifier_i2_List: identifier_i2*
        # nullable=True
        mark = self._mark()
        if (i1 := self._loop0_1(),):
            return i1
        self._reset(mark)
        return None

    @memoize
    def identifier_i2(self) -> Optional[Any]:
        # identifier_i2: '.' (&&(simpleIdentifier))
        mark = self._mark()
        if (self.expect(".")) and (
            i1 := self.expect_forced(self.simpleIdentifier(), """(simpleIdentifier)""")
        ):
            return i1
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
    def modifiers(self) -> Optional[AST.List[AST.Modifier]]:
        # modifiers: DEDENT?
        # nullable=True
        mark = self._mark()
        if (self.expect("DEDENT"),):
            return AST.List(elements=list())
        self._reset(mark)
        return None

    @memoize
    def packageHeader(self) -> Optional[AST.PackageHeader]:
        # packageHeader: 'package' (&&(identifier)) &&(semi)
        mark = self._mark()
        if (
            (self.expect("package"))
            and (i1 := self.expect_forced(self.identifier(), """(identifier)"""))
            and (self.expect_forced(self.semi(), """(semi)"""))
        ):
            return AST.PackageHeader(identifier=i1)
        self._reset(mark)
        return None

    @memoize
    def importList(self) -> Optional[AST.List[AST.ImportHeader]]:
        # importList: importHeader*
        # nullable=True
        mark = self._mark()
        if (_loop0_2 := self._loop0_2(),):
            return _loop0_2
        self._reset(mark)
        return None

    @memoize
    def importHeader(self) -> Optional[AST.ImportHeader]:
        # importHeader: 'import' (&&(identifier)) importHeader_i2 &&(semi)
        mark = self._mark()
        if (
            (self.expect("import"))
            and (i1 := self.expect_forced(self.identifier(), """(identifier)"""))
            and (i2 := self.importHeader_i2())
            and (self.expect_forced(self.semi(), """(semi)"""))
        ):
            return AST.ImportHeader(identifier=i1, alias=i2)
        self._reset(mark)
        return None

    @memoize
    def importHeader_i2(self) -> Optional[AST.ImportAlias | AST.Null]:
        # importHeader_i2: importAlias | '.' '*' | DEDENT?
        # nullable=True
        mark = self._mark()
        if importAlias := self.importAlias():
            return importAlias
        self._reset(mark)
        if (self.expect(".")) and (self.expect("*")):
            return AST.ImportAlias()
        self._reset(mark)
        if (self.expect("DEDENT"),):
            return AST.Null()
        self._reset(mark)
        return None

    @memoize
    def importAlias(self) -> Optional[AST.ImportAlias]:
        # importAlias: 'as' (&&(simpleIdentifier))
        mark = self._mark()
        if (self.expect("as")) and (
            i1 := self.expect_forced(self.simpleIdentifier(), """(simpleIdentifier)""")
        ):
            return AST.ImportAlias(identifier=i1)
        self._reset(mark)
        return None

    @memoize
    def semi(self) -> Optional[AST.TokenWrapper]:
        # semi: NEWLINE | ';'
        mark = self._mark()
        if _newline := self.expect("NEWLINE"):
            return _newline
        self._reset(mark)
        if literal := self.expect(";"):
            return literal
        self._reset(mark)
        return None

    @memoize
    def topLevelObjectList(self) -> Optional[AST.List[AST.Declaration]]:
        # topLevelObjectList: topLevelObject*
        # nullable=True
        mark = self._mark()
        if (i1 := self._loop0_3(),):
            return i1
        self._reset(mark)
        return None

    @memoize
    def topLevelObject(self) -> Optional[AST.Declaration]:
        # topLevelObject: declaration &&(semi)
        mark = self._mark()
        if (i1 := self.declaration()) and (
            self.expect_forced(self.semi(), """(semi)""")
        ):
            return i1
        self._reset(mark)
        return None

    @memoize
    def declaration(self) -> Optional[AST.Declaration]:
        # declaration: functionDeclaration
        mark = self._mark()
        if functionDeclaration := self.functionDeclaration():
            return functionDeclaration
        self._reset(mark)
        return None

    @memoize
    def receiverType(self) -> Optional[AST.ReceiverType]:
        # receiverType: parenthisedType | typeReference
        mark = self._mark()
        if parenthisedType := self.parenthisedType():
            return parenthisedType
        self._reset(mark)
        if typeReference := self.typeReference():
            return typeReference
        self._reset(mark)
        return None

    @memoize
    def parenthisedType(self) -> Optional[AST.ParenthisedType]:
        # parenthisedType: '(' type ')'
        mark = self._mark()
        if (
            (literal := self.expect("("))
            and (type := self.type())
            and (literal_1 := self.expect(")"))
        ):
            return [literal, type, literal_1]
        self._reset(mark)
        return None

    @memoize
    def typeReference(self) -> Optional[Any]:
        # typeReference: userType
        mark = self._mark()
        if userType := self.userType():
            return userType
        self._reset(mark)
        return None

    @memoize
    def userType(self) -> Optional[Any]:
        # userType: simpleUserType
        mark = self._mark()
        if simpleUserType := self.simpleUserType():
            return simpleUserType
        self._reset(mark)
        return None

    @memoize
    def type(self) -> Optional[Any]:
        # type: DEDENT
        mark = self._mark()
        if _dedent := self.expect("DEDENT"):
            return _dedent
        self._reset(mark)
        return None

    @memoize
    def simpleUserType(self) -> Optional[Any]:
        # simpleUserType: DEDENT
        mark = self._mark()
        if _dedent := self.expect("DEDENT"):
            return _dedent
        self._reset(mark)
        return None

    @memoize
    def _loop0_1(self) -> Optional[Any]:
        # _loop0_1: identifier_i2
        mark = self._mark()
        children = []
        while identifier_i2 := self.identifier_i2():
            children.append(identifier_i2)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_2(self) -> Optional[Any]:
        # _loop0_2: importHeader
        mark = self._mark()
        children = []
        while importHeader := self.importHeader():
            children.append(importHeader)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_3(self) -> Optional[Any]:
        # _loop0_3: topLevelObject
        mark = self._mark()
        children = []
        while topLevelObject := self.topLevelObject():
            children.append(topLevelObject)
            mark = self._mark()
        self._reset(mark)
        return children

    KEYWORDS = ("as", "fun", "import", "package")
    SOFT_KEYWORDS = ()
