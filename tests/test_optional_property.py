from optional import OptionalProperty, optionalproperty

_DEFAULT_NUM = 45


class _TestClass:
    @optionalproperty
    def number(self) -> int:
        return _DEFAULT_NUM


def test_get_descriptor():
    assert isinstance(_TestClass.number, OptionalProperty)


def test_default_value():
    obj = _TestClass()
    assert obj.number == _DEFAULT_NUM


def test_set_value():
    obj = _TestClass()
    number = 33
    obj.number = number
    assert obj.number == number


def test_property_is_present():
    obj = _TestClass()
    assert not _TestClass.number.is_present(obj)
    obj.number = 20
    assert _TestClass.number.is_present(obj)


def test_property_delete():
    obj = _TestClass()
    obj.number = 33
    del obj.number
    assert not _TestClass.number.is_present(obj)
