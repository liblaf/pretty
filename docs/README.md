# Pretty

`liblaf.pretty` formats Python objects as repr-like output. Use it when you
want compact plain text for logs and snapshots, or a Rich renderable that wraps
against the target console width.

## Quick Start

`pformat()` returns plain text:

```python
from liblaf.pretty import pformat

print(pformat({"alpha": [1, 2, 3]}), end="")
```

```text
{'alpha': [1, 2, 3]}
```

Use `plower()` when you need Rich to choose the layout later:

```python
from rich.console import Console

from liblaf.pretty import plower

console = Console(
    width=12,
    color_system=None,
    soft_wrap=True,
    no_color=True,
    markup=False,
    emoji=False,
    highlight=False,
)

print(plower({"alpha": [1, 2, 3]}).to_plain(console=console), end="")
```

```text
{
|   'alpha': [
|   |   1,
|   |   2, 3
|   ]
}
```

If you already have a Rich console, `pprint()` and its alias `pp()` format and
print in one call.

## Formatting Options

The public helpers accept the same keyword overrides:

| Keyword | Default | Meaning |
| --- | --- | --- |
| `max_level` | `6` | Maximum nesting depth before children collapse to `...`. |
| `max_list` | `6` | Maximum visible items in list-like containers. |
| `max_array` | `5` | Maximum array items forwarded to repr-style handlers. |
| `max_dict` | `4` | Maximum visible key-value pairs in mappings. |
| `max_string` | `30` | Maximum string repr length before truncation. |
| `max_long` | `40` | Maximum integer repr length before truncation. |
| `max_other` | `30` | Maximum repr length for other scalar values. |
| `indent` | `"|   "` | Indentation used when layouts break across lines. |
| `hide_defaults` | `True` | Hide default-valued `fieldz` and `__rich_repr__` fields. |

Each value can also come from a `PRETTY_*` environment variable. For example,
`PRETTY_MAX_LIST=1` has the same effect as `pformat(obj, max_list=1)`.

`indent` accepts plain text, Rich markup, ANSI-colored text, or
`rich.text.Text`.

## Built In

`liblaf.pretty` handles these cases without extra registration:

- scalar values through bounded repr output
- `dict`, `list`, `tuple`, `set`, and `frozenset`
- `fieldz`-compatible models, including common `attrs` classes
- objects with `__rich_repr__`
- fallback repr output for everything else

`hide_defaults=True` applies to both `fieldz`-compatible models and
`__rich_repr__` output:

```python
import attrs

from liblaf.pretty import pformat


@attrs.define
class Point:
    x: int = 1
    y: int = 2


print(pformat(Point()))
print(pformat(Point(), hide_defaults=False), end="")
```

```text
Point()
Point(x=1, y=2)
```

Objects with `__rich_repr__` can mix named and positional items. Falsey names
fall back to positional output, so `("", value)` and `(None, value)` render the
same way as explicit positional items.

## Reference Tracking

Referencable objects can be annotated on first appearance and replaced by
`<Type @ hexid>` later. This keeps recursive and shared structures readable
without losing identity information.

```python
from liblaf.pretty import pformat

child = {"x": 1}
print(pformat({"left": child, "right": child}), end="")
```

```text
{
|   'left': {'x': 1},  # <dict @ 7fe2adb72ec0>
|   'right': <dict @ 7fe2adb72ec0>
}
```

Lists and tuples repeat their value instead of becoming reference tags. Custom
containers are referencable by default, and custom leaves can opt in or out.

## Custom Formatting

Use the smallest hook that matches the object you want to format:

- Implement `__pretty__(self, ctx)` when you own the class.
- Use `register_type()` for a concrete class and its subclasses.
- Use `register_func()` for structural matching.
- Use `register_lazy()` for optional dependencies that should only activate
  after their module is already imported.

`PrettyContext` gives custom formatters the builder helpers they usually need:
`ctx.container()`, `ctx.leaf()`, `ctx.positional()`, `ctx.name_value()`, and
`ctx.key_value()`.

See [Custom Formatters](guides/custom-formatters.md) for examples.

## Pipeline

The public path is:

1. `plower()` wraps the object, traces shared references, and lowers the result.
2. Rich renders the lowered object against a `Console`.
3. `pformat()` captures that renderable as plain text with a safe default
   console.

The `stages.wrapped`, `stages.traced`, and `stages.lowered` packages expose the
pipeline pieces for maintainers and advanced integrations. Most users only need
the public helpers and `PrettyContext`.

See the [API reference](reference/liblaf/pretty/README.md) for signatures and
source-backed docstrings.
