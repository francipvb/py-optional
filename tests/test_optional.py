from typing import Any
from unittest.mock import AsyncMock, Mock

from optional import Optional, ValueNotProvidedError
from pytest import mark, raises


class TestEmptyOptional:
    def test_two_empty_are_equal(self):
        o1: Optional[Any] = Optional.empty()
        o2: Optional[Any] = Optional.empty()
        assert o1 == o2

    def test_two_optionals_are_different(self):
        o1: Optional[Any] = Optional.empty()
        o2: Optional[Any] = Optional.empty()
        assert o1 is not o2

    def test_empty_optional_is_false(self):
        optional: Optional[Any] = Optional.empty()
        assert not optional

    def test_or_else(self):
        optional: Optional[int] = Optional.empty().or_else(44)
        assert optional.value == 44
        assert optional.has_value

    def test_empty_optional_raises_exception(self):
        optional: Optional[Any] = Optional.empty()
        with raises(ValueNotProvidedError):
            optional.value

    def test_repr(self):
        optional: Optional[int] = Optional.empty()
        assert repr(optional) == "Optional.empty()"

    def test_str(self):
        optional: Optional[int] = Optional.empty()
        assert str(optional) == "empty"

    def test_has_value_false(self):
        optional = Optional.empty()
        assert not optional.has_value

    def test_is_empty(self):
        optional = Optional.empty()
        assert optional.is_empty


class TestValueOptional:
    def test_none_value_optional_is_true(self):
        optional = Optional.of(None)
        assert optional

    def test_two_optional_are_equal_with_same_value(self):
        optional1 = Optional.of(4.3)
        optional2 = Optional.of(4.3)
        assert optional1 == optional2

    def test_optional_return_value(self):
        optional = Optional.of(42)
        assert optional.value == 42

    def test_or_else_return_value(self):
        optional = Optional.of(45)
        assert optional.or_else(43).value == 45

    def test_has_value(self):
        optional = Optional.of(5)
        assert optional.has_value

    def test_repr(self):
        optional = Optional.of(5)
        assert repr(optional) == "Optional[int].of(5)"

    def test_str(self):
        optional = Optional.of("test")
        assert str(optional) == "test"

    def test_not_equal_optionals(self):
        optional1 = Optional.of(43)
        optional2 = Optional.of(44)
        assert optional1 != optional2

    def test_not_equal_optionals_false(self):
        optional1 = Optional.of(43)
        optional2 = Optional.of(43)
        assert not (optional1 != optional2)

    def test_not_empty(self):
        optional = Optional.of(45)
        assert not optional.is_empty

    def test_incompatible_equality(self):
        opt_value = Optional.of(45)
        assert opt_value != "test"


def test_equal():
    opt_value = Optional.of(45)
    opt_empty: Optional[int] = Optional.empty()
    assert opt_value != opt_empty


class TestMap:
    def test_map_empty(self):
        empty_optional: Optional[int] = Optional.empty()
        with raises(ValueNotProvidedError):
            assert empty_optional.map(lambda x: x * 2).value

    def test_map_value(self):
        mapper = Mock(return_value=66)
        value = Optional.of(33).map(mapper)
        mapper.assert_not_called()
        assert value.value == 66
        mapper.assert_called_with(33)

    def test_has_value(self):
        mapper = Mock()
        empty_optional: Optional[int] = Optional.empty().map(mapper)
        value_optional = Optional.of(45).map(mapper)
        assert not empty_optional.has_value
        assert value_optional.has_value

    def test_repr(self):
        mapper = Mock()
        empty_optional: Optional[int] = Optional.empty().map(mapper)
        assert repr(empty_optional) == f"Optional.empty().map({mapper!r})"

    def test_str(self):
        mapper = Mock(return_value=44)
        empty_optional: Optional[int] = Optional.empty()
        value_optional = Optional.of(33).map(mapper)
        assert str(value_optional) == "44"
        assert str(empty_optional.map(mapper)) == str(empty_optional)


def test_str():
    assert str(Optional.empty().or_else(33)) == str(33)


def test_repr():
    assert repr(Optional.empty().or_else(33)) == "Optional.empty().or_else(33)"


class TestApply:
    def test_apply_empty(self):
        empty_value: Optional[int] = Optional.empty()
        func = Mock()
        else_func = Mock()
        empty_value.apply(func, if_empty=else_func)
        func.assert_not_called()
        else_func.assert_called_once()

    def test_apply(self):
        empty_value: Optional[int] = Optional.of(45)
        func = Mock()
        else_func = Mock()
        empty_value.apply(func, if_empty=else_func)
        func.assert_called_once_with(45)
        else_func.assert_not_called

    @mark.anyio()
    async def test_apply_async_empty(self):
        empty_value: Optional[int] = Optional.empty()
        func = AsyncMock()
        else_func = AsyncMock()
        await empty_value.apply_async(func, if_empty=else_func)
        func.assert_not_called()
        else_func.assert_called_once()
        else_func.assert_awaited()

    @mark.anyio()
    async def test_apply_async(self):
        empty_value: Optional[int] = Optional.of(45)
        func = AsyncMock()
        else_func = AsyncMock()
        await empty_value.apply_async(func, if_empty=else_func)
        func.assert_called_once_with(45)
        func.assert_awaited()
        else_func.assert_not_called
