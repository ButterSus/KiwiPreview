from __future__ import annotations

# IMPORTS
# =======>

# noinspection PyUnresolvedReferences
import typing
import pegen.parser as pegen

# EXPORTS
# =======>

__all__ = [
    'memoize',
    'memoize_left_rec',
]

# MAIN CONTENT
# ============>
F = typing.TypeVar("F", bound=typing.Callable[..., typing.Any])
P = typing.TypeVar("P", bound="Parser")
T = typing.TypeVar("T")


def memoize(method: F) -> F:
    """
    A wrapper for memoize from pegen.parser that overrides list type
    """
    method = pegen.memoize(method)

    def wrapper(self: pegen.Parser, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        result = method(self, *args, **kwargs)
        if isinstance(result, list):
            return memoize.List(elements=result)  # type: ignore
        return result

    return typing.cast(F, wrapper)


def memoize_left_rec(method: typing.Callable[[P], typing.Optional[T]]) -> typing.Callable[[P], typing.Optional[T]]:
    """
    A wrapper for memoize_left_rec from pegen.parser that overrides list type
    """
    method = pegen.memoize_left_rec(method)

    def wrapper(self: pegen.Parser, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        result = method(self, *args, **kwargs)  # type: ignore
        if isinstance(result, list):
            return memoize.List(elements=result)  # type: ignore
        return result

    return typing.cast(F, wrapper)
