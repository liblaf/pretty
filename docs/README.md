# Pretty

`liblaf.pretty` gives you repr-like output that stays readable when values get
large, nested, shared, or cyclic. The formatter builds a Rich renderable first,
then lets Rich decide the final layout for the active console width.

## Start With `pformat()`

```python
from rich.console import Console

from liblaf.pretty import pformat

rendered = pformat({"alpha": [1, 2, 3]})
console = Console(width=12, color_system=None, soft_wrap=True)

print(rendered.to_plain(console), end="")
```

```text
{
|   'alpha': [
|   |   1,
|   |   2, 3
|   ]
}
```

`pformat()` returns a Rich renderable, not a string. Use `console.print()` to
render it normally, or `.to_plain(console=...)` when you want deterministic
plain text for logs, tests, or snapshots.

If you already have a Rich console, `pprint()` and `pp()` format and print in
one step.

## Formatting Options

The public formatting functions accept these keyword overrides:

| Keyword | Default | Meaning |
| --- | --- | --- |
| `max_level` | `6` | Maximum nesting depth before values collapse to `...`. |
| `max_list` | `6` | Maximum visible items in list-like containers. |
| `max_array` | `5` | Maximum array items forwarded to repr-style handlers. |
| `max_dict` | `4` | Maximum visible key-value pairs in dictionaries. |
| `max_string` | `30` | Maximum string repr length before truncation. |
| `max_long` | `40` | Maximum integer repr length before truncation. |
| `max_other` | `30` | Maximum repr length for other scalar values. |
| `indent` | `"|   "` | Indentation used when layouts break across lines. |
| `hide_defaults` | `True` | Hide default-valued fields from `attrs` and `__rich_repr__` output. |

Each value can also come from `PRETTY_*` environment variables. For example,
`PRETTY_MAX_LIST=1` has the same effect as `pformat(obj, max_list=1)`.

Width is chosen when Rich renders the result through a `Console`, not when you
call `pformat()`.

## Supported Integrations

- Builtin containers such as `dict`, `list`, `tuple`, `set`, and `frozenset`
- Repr-style truncation for deep, wide, or long values
- `attrs` and `fieldz` objects
- Objects with `__rich_repr__`
- Shared and cyclic references
- Custom handlers via `register_type()`, `register_func()`, `register_lazy()`,
  or `__pretty__(self, ctx)`

Repeated references are turned into tagged references instead of expanding the
same object forever. The first occurrence is annotated, and later occurrences
render as `<Type @ hexid>` references.

## Extending The Formatter

Use `register_type()` when you want a handler for one concrete class:

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

`ctx.container()` adds the type name for referencable objects, so custom
handlers usually supply only punctuation such as `(` and `)`.

For a deeper guide, see [Custom Formatters](guides/custom-formatters.md).

## Pipeline

The public API is small:

- `pformat()` builds a lowered Rich renderable.
- `pprint()` and `pp()` print that renderable through a `Console`.
- `PrettyContext` and the registration helpers power custom integrations.

The lower-level `stages.wrapped`, `stages.traced`, and `stages.lowered` modules
are part of the internal pipeline and are mostly useful when you are extending
the formatter itself.

See the [API reference](reference/liblaf/pretty/README.md) for signatures and
source-backed docstrings.
