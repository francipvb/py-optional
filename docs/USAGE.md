# Detailed usage instructions

## Importing

If you use the typing support for python, you know about the `Optional` python type marker. For this reason, you may encounter issues when using this library.

To avoid this issue, you can import the class with an alias for disambiguation:

```{py title="Example importing"}
from optional import Optional as O

```

## Empty values

Main purpose for empty values are to be supplied as default function parameter values, like the below example:

```python
from typing import Dict, Any

from optional import Optional as O

def test_function(
    *,
    value1: O[int] = O.empty(),
    value2: O[float] = O.empty(),
) -> Dict[str, Any]:
    data = {}
    if value1.has_value:
        data.update(value1=value1.value)

    if value_2.has_value:
        data.update(value2=value2.value)

    return data

```

In the previous example, if you provide a value for any predefined parameter, you'll get it inserted in the dict, even if it is set to None.

## Optional values

An `Optional` object, if not empty, wraps a value. The value can be anything, including `None` values.

For example, if you want to call the function we've defined above, we do something like this:

```python
test_func(value1=O.of(2)) # {'value1': 2}
```

## The `or_else` method

Sometimes you require a value for a function call. For this situation, there is a method called `or_else` in every Optional object.

This method returns a new **Optional** object with some differences to the two other values:

- If the source object has a value, this value is returned.
- if the source is an empty **Optional**, the `value` property returns the supplied value.

For example:

```pycon
>>> from optional import Optional as O
>>> O.empty().or_else(45).value
45
>>> O.of(33).or_else(45).value
33
>>>
```

## The `map` method

Another functionality of the **Optional** objects is the `map` method. Again, this method returns a new **Optional** object with custom behavior:

- The `has_value` and `is_empty` reflects the values of the source **Optional** object.
- The `value` object runs a function, providing the result of the source `value` property.

The implications of the last point is that you can chain `map` method calls to subsequently transform the value, and the callable won't run until you access the `value` property. However, if any of the source **Optional** objects is empty, you'll get an exception raised.

To prevent this, you can call the `or_else` method on the new **Optional** object.

## The `apply` and `apply_async` methods

These methods have a similar purpose. The only difference is that the `apply_async` method should be called when an async operation should be done for the **Optional** value.

## The **optionalproperty** decorator

This decorator returns a **OptionalProperty** object.

The **OptionalProperty** decorator is a
descriptor emulating a property with a default
value. If a value is not set, a callable is
executed to provide the default value.

The descriptor also has a method to check wether the value is set in a specific object
instance.

See the optional property [decorator][optional.optionalproperty] and [class][optional.OptionalProperty] documentation for details.
