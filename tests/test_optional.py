from typing import Any
from unittest.mock import AsyncMock, Mock

from optional import Optional, ValueNotProvidedError
from optional.optional import Empty, Of
from pytest import mark, raises


class TestEmptyOptional:
    def test_two_empty_are_equal(self) -> None:
        o1: Optional[Any] = Empty()
        o2: Optional[Any] = Empty()
        assert o1 == o2

    def test_two_optionals_are_different(self) -> None:
        o1: Optional[Any] = Empty()
        o2: Optional[Any] = Empty()
        assert o1 is not o2

    def test_empty_optional_is_false(self) -> None:
        optional: Optional[Any] = Empty()
        assert not optional

    def test_or_else(self) -> None:
        optional: Optional[int] = Empty().or_else(44)
        assert optional.value == 44
        assert optional.has_value

    def test_empty_optional_raises_exception(self) -> None:
        optional: Optional[Any] = Empty()
        with raises(ValueNotProvidedError):
            optional.value

    def test_repr(self) -> None:
        optional: Optional[int] = Empty()
        assert repr(optional) == "Empty()"

    def test_str(self) -> None:
        optional: Optional[int] = Empty()
        assert str(optional) == "empty"

    def test_has_value_false(self) -> None:
        optional: Optional[Any] = Empty()
        assert not optional.has_value

    def test_is_empty(self) -> None:
        optional = Empty()
        assert optional.is_empty


class TestValueOptional:
    def test_none_value_optional_is_true(self) -> None:
        optional = Of(None)
        assert optional

    def test_two_optional_are_equal_with_same_value(self) -> None:
        optional1 = Of(4.3)
        optional2 = Of(4.3)
        assert optional1 == optional2

    def test_optional_return_value(self) -> None:
        optional = Of(42)
        assert optional.value == 42

    def test_or_else_return_value(self) -> None:
        optional = Of(45)
        assert optional.or_else(43).value == 45

    def test_has_value(self) -> None:
        optional = Of(5)
        assert optional.has_value

    def test_repr(self) -> None:
        optional = Of(5)
        assert repr(optional) == "Of(5)"

    def test_str(self) -> None:
        optional = Of("test")
        assert str(optional) == "test"

    def test_not_equal_optionals(self) -> None:
        optional1 = Of(43)
        optional2 = Of(44)
        assert optional1 != optional2

    def test_not_equal_optionals_false(self) -> None:
        optional1 = Of(43)
        optional2 = Of(43)
        assert not (optional1 != optional2)

    def test_not_empty(self) -> None:
        optional = Of(45)
        assert not optional.is_empty

    def test_incompatible_equality(self) -> None:
        opt_value = Of(45)
        assert opt_value != "test"


def test_equal() -> None:
    opt_value = Of(45)
    opt_empty: Optional[int] = Empty()
    assert opt_value != opt_empty


class TestMap:
    def test_map_empty(self) -> None:
        empty_optional: Optional[int] = Empty()
        with raises(ValueNotProvidedError):
            assert empty_optional.map(lambda x: x * 2).value

    def test_map_value(self) -> None:
        mapper = Mock(return_value=66)
        value = Of(33).map(mapper)
        mapper.assert_not_called()
        assert value.value == 66
        mapper.assert_called_with(33)

    def test_has_value(self) -> None:
        mapper = Mock()
        empty_optional: Optional[int] = Empty().map(mapper)
        value_optional = Of(45).map(mapper)
        assert not empty_optional.has_value
        assert value_optional.has_value

    def test_repr(self) -> None:
        mapper = Mock()
        empty_optional: Optional[int] = Empty().map(mapper)
        assert repr(empty_optional) == f"Empty().map({mapper!r})"

    def test_str(self) -> None:
        mapper = Mock(return_value=44)
        empty_optional: Optional[int] = Empty()
        value_optional = Of(33).map(mapper)
        assert str(value_optional) == "44"
        assert str(empty_optional.map(mapper)) == str(empty_optional)


def test_str() -> None:
    assert str(Empty().or_else(33)) == str(33)


def test_repr() -> None:
    assert repr(Empty().or_else(33)) == "Empty().or_else(33)"


class TestApply:
    def test_apply_empty(self) -> None:
        empty_value: Optional[int] = Empty()
        func = Mock()
        else_func = Mock()
        empty_value.apply(func, if_empty=else_func)
        func.assert_not_called()
        else_func.assert_called_once()

    def test_apply(self) -> None:
        empty_value: Optional[int] = Of(45)
        func = Mock()
        else_func = Mock()
        empty_value.apply(func, if_empty=else_func)
        func.assert_called_once_with(45)
        else_func.assert_not_called

    @mark.anyio()
    async def test_apply_async_empty(self) -> None:
        empty_value: Optional[int] = Empty()
        func = AsyncMock()
        else_func = AsyncMock()
        await empty_value.apply_async(func, if_empty=else_func)
        func.assert_not_called()
        else_func.assert_called_once()
        else_func.assert_awaited()

    @mark.anyio()
    async def test_apply_async(self) -> None:
        empty_value: Optional[int] = Of(45)
        func = AsyncMock()
        else_func = AsyncMock()
        await empty_value.apply_async(func, if_empty=else_func)
        func.assert_called_once_with(45)
        func.assert_awaited()
        else_func.assert_not_called
