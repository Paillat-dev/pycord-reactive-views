# Copyright (c) Paillat-dev
# SPDX-License-Identifier: MIT

from collections.abc import Awaitable, Callable
from inspect import isawaitable
from typing import Generic, Literal, TypeGuard, TypeVar

T = TypeVar("T")


class Unset:
    """A class to represent an unset value."""

    def __bool__(self) -> Literal[False]:
        return False


UNSET = Unset()


class ReactiveValue(Generic[T]):
    """A value that can be a constant, a callable, or an async callable."""

    def __init__(self, func: Callable[[], T] | Callable[[], Awaitable[T]], default: T | Unset = UNSET) -> None:
        """Create a new reactive value."""
        self._func: Callable[[], T] | Callable[[], Awaitable[T]] = func
        self.default: T | Unset = default

    async def __call__(self) -> T:
        """Call the function and return the value.

        :raises TypeError: If the value is not callable
        """
        if callable(self._func):
            ret = self._func()
            if isawaitable(ret):
                return await ret
            return ret
        raise TypeError("ReactiveValue must be a callable")


MaybeReactiveValue = T | ReactiveValue[T]


def is_reactive(value: MaybeReactiveValue[T]) -> TypeGuard[ReactiveValue[T]]:
    """Check if a value is a reactive value."""
    return isinstance(value, ReactiveValue)
