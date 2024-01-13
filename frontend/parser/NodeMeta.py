from __future__ import annotations

# IMPORTS
# =======>

# noinspection PyUnresolvedReferences
import typing
from abc import ABCMeta
from dataclasses import field, dataclass
from enum import Enum, auto
import re

# EXPORTS
# =======>
__all__ = [
    'NodeMeta',
    'MetaEffect',
    'MetaEffectWrapper',
    'meta_effect'
]

# MAIN CONTENT
# ============>
if typing.TYPE_CHECKING:
    from frontend.parser.AST import Node


class NodeMeta(ABCMeta):
    """
    Metaclass for all nodes

    This metaclass adds the following fields to the class:
    - name: str = field(default=name, init=False, repr=True, compare=True)
    - row: int = field(init=False, repr=False, compare=True)
    - column: int = field(init=False, repr=False, compare=True)
    - end_row: int = field(init=False, repr=False, compare=True)
    - end_column: int = field(init=False, repr=False, compare=True)

    It also modifies a post_init method that sets the row and column fields to the row and column of the first child

    Attributes
    ----------
    _initialized_classes: typing.Dict[str, typing.Tuple[type]]
        A dictionary of all classes that have been initialized, used to know which classes are inherited from
        parentbase classes

    Notes
    -----
    Use `is_base=True` to create a base class (i.e. an abstract class).
    All non-base classes should have a `base` argument.

    Use `no_track=True` to disable the row and column tracking.
    This is useful for classes that are not nodes.
    """

    _initialized_classes: typing.Dict[str, typing.Tuple[type]] = dict()

    def __new__(mcs, name, bases, namespace, **kwargs):
        """
        Overrides the __new__ method of the metaclass

        Parameters
        ----------
        mcs: NodeMeta
            The metaclass
        name: str
            The name of the class
        bases: typing.Tuple[type]
            The base classes
        namespace: typing.Dict[str, typing.Any]
            The namespace of the class

        Returns
        -------
        Node
            The new class
        """
        # Add to initialized classes
        # ------------------------->
        if name not in mcs._initialized_classes:
            mcs._initialized_classes[name] = bases

        # Add name field
        # -------------->
        post_kwargs = {
            k: v for k, v in kwargs.items() if k not in {'is_base', 'base', 'no_track'}
        }
        namespace['name'] = field(default=name, init=False, repr=True, compare=True)
        children: typing.List[typing.Any] = list()
        namespace['children'] = field(default_factory=lambda: children, init=False, repr=False, compare=False)
        if kwargs.get('is_base', False):
            # noinspection PyTypeChecker
            return super().__new__(mcs, name, bases, namespace, **post_kwargs)
        if kwargs.get('base', None) is None:
            raise ValueError('Non-base classes must have a base')
        parentbase = kwargs['base']
        if '__annotations__' not in namespace:
            namespace['__annotations__'] = dict()
        if 'name' not in namespace['__annotations__']:
            namespace['__annotations__']['name'] = 'str'
        if 'children' not in namespace['__annotations__']:
            namespace['__annotations__']['children'] = typing.List[str]

        # Row and column fields
        # --------------------->
        def lazy_init():
            def isValidAttribute(key: str, annotations) -> bool:
                value: str = annotations.get(key, None)
                if isinstance(value, str):
                    value = re.sub(r"\[(.*?)]", str(), value)
                if isinstance(value, MetaEffectWrapper):
                    effectWrapper: MetaEffectWrapper = value
                    if MetaEffect.IGNORED_FIELD in value.effects:
                        return False
                    annotations[key] = effectWrapper.value
                    return isValidAttribute(key, annotations)
                if not isinstance(value, str):
                    return False
                for value in map(str.strip, value.split('|')):
                    value_bases = mcs._initialized_classes.get(value, tuple())
                    if any([issubclass(value_base, parentbase) for value_base in value_bases]):
                        return True
                return False

            nonlocal children
            new_set = set()
            for base in bases:
                if hasattr(base, '__annotations__'):
                    new_set.update(
                        filter(
                            lambda x: isValidAttribute(x, base.__annotations__),
                            base.__annotations__.keys()
                        )
                    )
            new_set.update(
                filter(
                    lambda x: isValidAttribute(x, namespace['__annotations__']),
                    namespace['__annotations__'].keys()
                )
            )
            new_set.discard('name')
            new_set.discard('children')
            children.extend(new_set)

        if 'row' not in namespace['__annotations__']:
            namespace['__annotations__']['row'] = 'int'
        namespace['row'] = field(init=False, repr=False, compare=True)
        if 'column' not in namespace['__annotations__']:
            namespace['__annotations__']['column'] = 'int'
        namespace['column'] = field(init=False, repr=False, compare=True)
        if 'end_row' not in namespace['__annotations__']:
            namespace['__annotations__']['end_row'] = 'int'
        namespace['end_row'] = field(init=False, repr=False, compare=True)
        if 'end_column' not in namespace['__annotations__']:
            namespace['__annotations__']['end_column'] = 'int'
        namespace['end_column'] = field(init=False, repr=False, compare=True)
        namespace['_was_lazy_init'] = False
        post_init = namespace.get('__post_init__', lambda self: None)

        def post_init_wrapper(self):
            post_init(self)
            class_object = type(self)
            # noinspection PyProtectedMember
            if not class_object._was_lazy_init:
                lazy_init()
                class_object._was_lazy_init = True

            # Row and column
            # -------------->
            if (
                    self.row is not None and
                    self.column is not None and
                    self.end_row is not None and
                    self.end_column is not None
            ):
                return
            first_child = next(
                filter(
                    lambda x: hasattr(x, 'row') and hasattr(x, 'column'),
                    map(lambda key: self.__getattribute__(key), children)),
                None
            )
            last_child = next(
                filter(
                    lambda x: hasattr(x, 'end_row') and hasattr(x, 'end_column'),
                    map(lambda key: self.__getattribute__(key), reversed(children))),
                None
            )

            if first_child is None or last_child is None:
                raise (ValueError('Node must have at least one child with row '
                                  'and column and one child with end row and end column'))
            first_child: typing.Optional[Node]
            last_child: typing.Optional[Node]
            self.row = self.row if self.row is not None else first_child.row
            self.column = self.column if self.column is not None else first_child.column
            self.end_row = self.end_row if self.end_row is not None else last_child.end_row
            self.end_column = self.end_column if self.end_column is not None else last_child.end_column

        if not kwargs.get('no_track', False):
            namespace['__post_init__'] = post_init_wrapper
        # noinspection PyTypeChecker
        return super().__new__(mcs, name, bases, namespace, **post_kwargs)


class MetaEffect(Enum):
    IGNORED_FIELD = auto()


_T = typing.TypeVar('_T')


@dataclass
class MetaEffectWrapper:
    value: typing.Any
    effects: typing.Tuple[MetaEffect, ...]


def meta_effect(value: _T, *effects: MetaEffect) -> _T:
    return MetaEffectWrapper(value, effects)
