# Pretty

`liblaf.pretty` builds repr-like Rich renderables for Python objects. It is a
good fit for interactive debugging, logs, doctests, and snapshots where you
want readable output without giving up Rich styling or width-aware wrapping.

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
| `hide_defaults` | `True` | Hide default-valued fields from `fieldz` and `__rich_repr__` output. |

Each value can also come from `PRETTY_*` environment variables. For example,
`PRETTY_MAX_LIST=1` has the same effect as `pformat(obj, max_list=1)`.

`indent` accepts either a `str` or `rich.text.Text`. String values are parsed as
Rich markup, and ANSI escapes are preserved.

Width is chosen when Rich renders the result through a `Console`, not when you
call `pformat()`.

## Built-in Integrations

`liblaf.pretty` ships with a few integrations before you register anything:

- builtin containers such as `dict`, `list`, `tuple`, `set`, and `frozenset`
- `fieldz`-compatible models, including `attrs` models
- objects with `__rich_repr__`
- fallback repr output for everything else

`hide_defaults=True` applies to both `fieldz`-compatible models and
`__rich_repr__` output:

```python
import attrs
from rich.console import Console

from liblaf.pretty import pformat


@attrs.define
class Point:
    x: int = 1
    y: int = 2


console = Console(width=80, color_system=None, soft_wrap=True)

print(pformat(Point()).to_plain(console))
print(pformat(Point(), hide_defaults=False).to_plain(console), end="")
```

```text
Point()
Point(x=1, y=2)
```

Objects with `__rich_repr__` can mix named and positional items, and they use
the same default-hiding behavior.

## Reference Tracking

The formatter avoids infinite recursion and can annotate repeated references for
referencable objects such as mappings, sets, frozensets, and custom containers.
The first occurrence is annotated, and later occurrences render as
`<Type @ hexid>` references.

Scalar values and sequence literals still render safely, but they may repeat
their value instead of emitting a shared-reference marker.

## Environment Defaults

Per-call keyword overrides are usually the clearest choice, but you can also
set environment defaults with `PRETTY_*` variables:

```bash
export PRETTY_MAX_LIST=2
export PRETTY_INDENT='[bold]>>[/] '
```

`PRETTY_INDENT` accepts the same plain-text, Rich-markup, and ANSI-colored
strings as the `indent=` keyword argument.

## Extending The Formatter

The extension surface is intentionally small:

- Implement `__pretty__(self, ctx)` when you own the class.
- Use `register_type()` for one concrete type and its subclasses.
- Use `register_func()` for structural handlers that decide at runtime whether
  they apply.
- Use `register_lazy()` when the target type lives in an optional dependency and
  should only activate after that module is already imported.

Here is a `register_type()` example:

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
handlers usually provide only punctuation and child items.

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
