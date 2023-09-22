from __future__ import annotations
import weakref
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Generic, Self, TypeVar, overload

from .optional import Optional

_V = TypeVar("_V")


class OptionalProperty(Generic[_V]):
    def __init__(
        self,
        fget: Callable[[Any], _V],
        doc: str | None = None,
    ) -> None:
        super().__init__()
        self._values: dict[int, _Entry[_V]] = {}
        self.__doc__ = __doc__ or fget.__doc__
        self.__func__ = fget

    @overload
    def __get__(self, instance: None, owner: type[Any]) -> Self:  # pragma: nocover
        ...

    @overload
    def __get__(self, instance: Any, owner: type[Any]) -> _V:  # pragma: nocover
        ...

    def __get__(self, instance: object | None, owner: type[Any]) -> _V | Self:
        if instance is not None:
            entry = self._entry(instance)
            if entry.value.has_value:
                return entry.value.value
            return self.__func__(instance)
        return self

    def __set__(self, __instance: Any, __value: _V) -> None:
        self._entry(__instance).value = Optional.of(__value)

    def _entry(self, obj: object) -> _Entry[_V]:
        entry = self._values.get(id(obj))
        if entry is None:

            def _finalyze(x: int) -> None:
                if x in self._values:
                    del self._values[x]

            entry = _Entry[_V](weakref.finalize(obj, _finalyze, id(obj)))
            self._values[id(obj)] = entry
        return entry

    def __delete__(self, instance: object) -> None:
        self._entry(instance).finalizer()

    def is_present(self, obj: object) -> bool:
        return self._entry(obj).value.has_value


@dataclass()
class _Entry(Generic[_V]):
    finalizer: weakref.finalize
    value: Optional[_V] = field(default_factory=Optional.empty)


def optionalproperty(func: Callable[[Any], _V]) -> OptionalProperty[_V]:
    return OptionalProperty(func)
