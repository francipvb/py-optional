from typing import Any

from pytest import raises

from optional import Optional, ValueNotProvidedError


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
        optional: Optional[int] = Optional.empty()
        assert optional.or_else(43) == 43

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
        assert optional.or_else(43) == 45

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
