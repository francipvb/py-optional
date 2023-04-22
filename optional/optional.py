"""The optional object implementation.

This module has the implementations for the **Optional** object.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, final

from .exceptions import ValueNotProvidedError

_T = TypeVar("_T")


class Optional(ABC, Generic[_T]):
    """An optional value wrapper."""

    __slots__ = ()

    @property
    @abstractmethod
    def value(self) -> _T:
        """Get the wrapped value.

        Raises:
            ValueNotProvidedError: If the value were not provided

        Returns:
            _T: The wrapped value
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def has_value(self) -> bool:
        """Get wether this object has a value in it.

        Returns:
            bool: Wether the value is present or not
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        """Get wether this instance is empty

        Returns:
            bool: `True` if the value is not present, `False` otherwise
        """
        raise NotImplementedError()

    @abstractmethod
    def or_else(self, value: _T) -> _T:
        """Return a value

        Args:
            value (_T): The value to retrieve if the instance is empty

        Returns:
            _T: The value
        """
        raise NotImplementedError()

    @staticmethod
    def of(value: _T) -> Optional[_T]:
        return _Value(value)

    @staticmethod
    def empty() -> Optional[Any]:
        return _Empty()


class _Empty(Optional[_T], Generic[_T]):
    @final
    @property
    def value(self) -> _T:
        raise ValueNotProvidedError("Value were not provided.")

    @final
    @property
    def has_value(self) -> bool:
        return False

    def __eq__(self, __value: object) -> bool:
        if type(__value) != type(self):
            return NotImplemented
        return True

    def or_else(self, value: _T) -> _T:
        return value

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "Optional.empty()"

    def __str__(self) -> str:
        return "empty"

    @property
    def is_empty(self) -> bool:
        return True


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

    def or_else(self, value: _T) -> _T:
        return self.value

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, type(self)):
            return NotImplemented

        # Delegate equality check to the instance values:
        return self.value == __value.value

    def __repr__(self) -> str:
        return f"Optional[{type(self.value).__qualname__}].of({self.value!r})"

    def __str__(self) -> str:
        return str(self.value)

    @property
    def is_empty(self) -> bool:
        return False
