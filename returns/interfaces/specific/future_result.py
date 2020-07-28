"""
Represents the base interfaces for types that do fearless async operations.

This type means that ``Future`` cannot fail.
Don't use this type for async that can. Instead, use
:class:`returns.interfaces.specific.future_result.FutureResultBasedN` type.
"""

from abc import abstractmethod
from typing import TYPE_CHECKING, Awaitable, Callable, NoReturn, Type, TypeVar

from returns.interfaces.specific import future, ioresult
from returns.primitives.hkt import KindN

if TYPE_CHECKING:
    from returns.future import Future, FutureResult  # noqa: WPS433

_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')

_FutureResultLikeType = TypeVar(
    '_FutureResultLikeType', bound='FutureResultLikeN',
)


class FutureResultLikeN(
    future.FutureLikeN[_FirstType, _SecondType, _ThirdType],
    ioresult.IOResultLikeN[_FirstType, _SecondType, _ThirdType],
):
    """
    Base type for ones that does look like ``FutureResult``.

    But at the time this is not a real ``Future`` and cannot be awaited.
    It is also cannot be unwrapped.
    """

    @abstractmethod
    def bind_future_result(
        self: _FutureResultLikeType,
        function: Callable[
            [_FirstType],
            'FutureResult[_UpdatedType, _SecondType]',
        ],
    ) -> KindN[_FutureResultLikeType, _UpdatedType, _SecondType, _ThirdType]:
        """Allows to bind ``FutureResult`` functions over a container."""

    @abstractmethod
    def bind_async_future_result(
        self: _FutureResultLikeType,
        function: Callable[
            [_FirstType],
            Awaitable['FutureResult[_UpdatedType, _SecondType]'],
        ],
    ) -> KindN[_FutureResultLikeType, _UpdatedType, _SecondType, _ThirdType]:
        """Allows to bind async ``FutureResult`` functions over container."""

    @classmethod
    @abstractmethod
    def from_failed_future(
        cls: Type[_FutureResultLikeType],  # noqa: N805
        inner_value: 'Future[_SecondType]',
    ) -> KindN[_FutureResultLikeType, _FirstType, _SecondType, _ThirdType]:
        """Creates new container from a failed ``Future``."""

    @classmethod
    def from_future_result(
        cls: Type[_FutureResultLikeType],  # noqa: N805
        inner_value: 'FutureResult[_FirstType, _SecondType]',
    ) -> KindN[_FutureResultLikeType, _FirstType, _SecondType, _ThirdType]:
        """Creates container from ``FutureResult`` instance."""


#: Type alias for kinds with one type argument.
FutureResultLike1 = FutureResultLikeN[_FirstType, NoReturn, NoReturn]

#: Type alias for kinds with two type arguments.
FutureResultLike2 = FutureResultLikeN[_FirstType, _SecondType, NoReturn]

#: Type alias for kinds with three type arguments.
FutureResultLike3 = FutureResultLikeN[_FirstType, _SecondType, _ThirdType]


class FutureResultBasedN(
    future.FutureBasedN[_FirstType, _SecondType, _ThirdType],
    FutureResultLikeN[_FirstType, _SecondType, _ThirdType],
):
    """
    Base type for real ``FutureResult`` objects.

    They can be awaited. Cannot be unwrapped.
    """


#: Type alias for kinds with one type argument.
FutureResultBased1 = FutureResultBasedN[_FirstType, NoReturn, NoReturn]

#: Type alias for kinds with two type arguments.
FutureResultBased2 = FutureResultBasedN[_FirstType, _SecondType, NoReturn]

#: Type alias for kinds with three type arguments.
FutureResultBased3 = FutureResultBasedN[_FirstType, _SecondType, _ThirdType]
