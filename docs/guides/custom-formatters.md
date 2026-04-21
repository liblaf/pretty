# Custom Formatters

`liblaf.pretty` gives you four ways to customize formatting:

- Implement `__pretty__(self, ctx)` when you own the type.
- Use `register_type()` for one concrete class.
- Use `register_func()` for structural handlers that may or may not apply.
- Use `register_lazy()` when the target type lives in an optional dependency.

## Choose A Hook

Use the smallest hook that matches the problem:

- `__pretty__()` keeps the formatting logic next to the model you own.
- `register_type()` is the normal choice for a concrete third-party class.
- `register_func()` is useful when you need structural matching instead of type
  matching.
- `register_lazy()` keeps optional integrations cheap because it waits for the
  dependency to be imported elsewhere.

## A Concrete Type

```python
from rich.text import Text

from liblaf.pretty import pformat, register_type


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


@register_type(Point)
def _pretty_point(obj: Point, ctx):
    return ctx.container(
        obj=obj,
        begin=Text("(", "repr.tag_start"),
        children=[ctx.name_value("x", obj.x), ctx.name_value("y", obj.y)],
        end=Text(")", "repr.tag_end"),
    )


print(pformat(Point(1, 2)).to_plain(), end="")
```

```text
Point(x=1, y=2)
```

`ctx.container()` prefixes the object's type name automatically for
referencable objects, so `begin` and `end` usually only need delimiters.

`register_type()` uses `functools.singledispatch`, so subclasses also match
unless you register something more specific.

## Owning The Type

If you control the class, `__pretty__(self, ctx)` keeps the formatting logic
next to the model:

```python
from rich.text import Text


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __pretty__(self, ctx):
        return ctx.container(
            obj=self,
            begin=Text("(", "repr.tag_start"),
            children=[ctx.name_value("x", self.x), ctx.name_value("y", self.y)],
            end=Text(")", "repr.tag_end"),
        )
```

The hook receives only `ctx`. Older `ctx, depth` examples are stale for this
package.

If `__pretty__` returns `None`, the registry keeps looking for other handlers.

## Building Output With `PrettyContext`

`PrettyContext` exposes a few helpers that are enough for most handlers:

- `ctx.leaf(obj, text)` builds a scalar node from a `rich.text.Text` value.
- `ctx.positional(value)` wraps one positional child.
- `ctx.name_value(name, value)` builds `name=value` output.
- `ctx.key_value(key, value)` builds `key: value` output.
- `ctx.container(obj=..., begin=..., children=..., end=...)` builds repr-like
  tagged containers.

Use `Text` for `begin`, `end`, and custom leaf output. Those values flow
through the Rich rendering pipeline and are not plain strings.

## Structural Registration

`register_func()` is useful when the handler should inspect an object and decide
at runtime whether it applies. Return `None` to let the next handler try.
Functional handlers run after type-based handlers and are checked in reverse
registration order, so the most recently registered handler wins.

## Lazy Registration

`register_lazy(module, name)` defers registration until that module has already
been imported. It does not import the module for you. This is a good fit for
optional dependencies such as array or tensor types that should not be imported
just for pretty-printing.

```python
from rich.text import Text

from liblaf.pretty import register_lazy


@register_lazy("numpy", "ndarray")
def _pretty_ndarray(obj, ctx):
    return ctx.leaf(
        obj,
        Text(f"ndarray(shape={obj.shape!r}, dtype={obj.dtype!s})", "repr.tag_name"),
        referencable=False,
    )
```

Once `numpy` is present in `sys.modules`, the handler is resolved and cached for
future formatting calls.
