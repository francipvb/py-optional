"""The optional object implementation.

This module has the implementations for the **Optional** object.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, TypeVar, final

from .exceptions import ValueNotProvidedError

_T = TypeVar("_T")
_TR = TypeVar("_TR")


class Optional(ABC, Generic[_T]):
    """An optional value wrapper."""

    __slots__ = ()

    @property
    @abstractmethod
    def value(self) -> _T:  # pragma: nocover
        """Get the wrapped value.

        Raises:
            ValueNotProvidedError: If the value were not provided

        Returns:
            _T: The wrapped value
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def has_value(self) -> bool:  # pragma: nocover
        """Get wether this object has a value in it.

        Returns:
            bool: Wether the value is present or not
        """
        raise NotImplementedError()

    @final
    @property
    def is_empty(self) -> bool:
        """Get wether this instance is empty

        Returns:
            bool: `True` if the value is not present, `False` otherwise
        """
        return not self.has_value

    @final
    def or_else(self, value: _T) -> Optional[_T]:
        """Return an optional value wrapping this.

        If this optional has a value, the value is returned. Otherwise, the supplied
        value is returned from the returned object's value propertyl.

        Args:
            value (_T): The value to retrieve if the instance is empty

        Returns:
            Optional[_T]: The `Optional` object wrapping this
        """

        return _Default(value, self)

    def map(self, mapper: Callable[[_T], _TR]) -> Optional[_TR]:
        return _Mapped(self, mapper)

    @staticmethod
    def of(value: _T) -> Optional[_T]:
        return _Value(value)

    @staticmethod
    def empty() -> Optional[Any]:
        return _Empty()

    def __eq__(self, __value: Any) -> bool:
        if type(__value) != type(self):
            return NotImplemented

        if self.has_value and __value.has_value:
            # Delegate comparison to value implementations itself.
            return self.value == __value.value

        # Compare the `has_value` property:
        return self.has_value == __value.has_value

    def __bool__(self) -> bool:
        return self.has_value


class _Empty(Optional[_T], Generic[_T]):
    @final
    @property
    def value(self) -> _T:
        raise ValueNotProvidedError("Value were not provided.")

    @final
    @property
    def has_value(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "Optional.empty()"

    def __str__(self) -> str:
        return "empty"


class _Value(Optional[_T], Generic[_T]):
    __slots__ = ("_value",)

    def __init__(self, value: _T) -> None:
        super().__init__()
        self._value = value

    @property
    def value(self) -> _T:
        return self._value

    @property
    def has_value(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"Optional[{type(self.value).__qualname__}].of({self.value!r})"

    def __str__(self) -> str:
        return str(self.value)


class _Mapped(Optional[_TR], Generic[_T, _TR]):
    __slots__ = ("_mapped", "_mapper", "_value", "_value_set")

    def __init__(self, mapped: Optional[_T], mapper: Callable[[_T], _TR]) -> None:
        self._mapper = mapper
        self._mapped = mapped
        self._value_set = False
        self._value = None

    @property
    def has_value(self) -> bool:
        return self._mapped.has_value

    @property
    def value(self) -> _TR:
        if not self._value_set:
            self._value = self._mapper(self._mapped.value)
            self._value_set = True

        return self._value  # type: ignore

    def __repr__(self) -> str:
        return f"{self._mapped!r}.map({self._mapper!r})"

    def __str__(self) -> str:
        if not self.has_value:
            return str(self._mapper)

        return str(self.value)


class _Default(Optional[_T], Generic[_T]):
    def __init__(self, value: _T, mapped: Optional[_T]) -> None:
        self._value = value
        self._mapped = mapped

    @property
    def value(self) -> _T:
        if self._mapped.has_value:
            return self._mapped.value

        return self._value

    @property
    def has_value(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"{self._mapped!r}.or_else({self._value!r})"
