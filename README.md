# ✨ Pretty

`liblaf.pretty` is a width-aware, repr-like pretty-printer for Python objects
built on [Rich](https://github.com/Textualize/rich).

[Guide](docs/README.md) ·
[Custom Formatters](docs/guides/custom-formatters.md) ·
[API Reference](https://liblaf.github.io/pretty/) ·
[Changelog](CHANGELOG.md)

## 📦 Install

```bash
uv add liblaf-pretty
# or
pip install liblaf-pretty
```

## 🚀 Quick Start

Use `pformat()` when you want a Rich renderable that can be printed directly or
converted to deterministic plain text for logs, tests, and snapshots:

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

If you already have a Rich console, use `pprint()` or its alias `pp()`:

```python
from liblaf.pretty import pprint

pprint({"alpha": [1, 2, 3]}, max_list=3)
```

## ✅ What It Handles

- Builtin containers such as `dict`, `list`, `tuple`, `set`, and `frozenset`
- `attrs` / `fieldz`-compatible models, with defaults hidden by default
- Objects with `__rich_repr__`
- Shared and cyclic references
- Per-call overrides plus environment-backed `PRETTY_*` defaults
- Custom hooks through `__pretty__()`, `register_type()`, `register_func()`,
  and `register_lazy()`

## 🎛️ Configuration

The public formatters accept these keyword overrides:

- `max_level`, `max_list`, `max_array`, `max_dict`
- `max_string`, `max_long`, `max_other`
- `indent`
- `hide_defaults`

Those overrides sit on top of environment-backed defaults loaded from
`PRETTY_*` variables:

```bash
export PRETTY_MAX_LIST=2
export PRETTY_INDENT='[bold]>>[/] '
```

`indent` accepts plain text, Rich markup, ANSI-colored strings, or
`rich.text.Text`.

## 🔁 Shared References

Referencable objects such as mappings, sets, frozensets, and custom containers
can be annotated when the same object appears more than once:

```python
from rich.console import Console

from liblaf.pretty import pformat

shared = {"x": 1}
rendered = pformat({"left": shared, "right": shared})
console = Console(width=80, color_system=None, soft_wrap=True)

print(rendered.to_plain(console), end="")
```

```text
{
|   'left': {'x': 1},  # <dict @ 7f...>
|   'right': <dict @ 7f...>
}
```

Sequence literals still render safely, but they may repeat their value instead
of becoming a shared-reference tag.

## 🧩 Custom Formatting

Builtin handlers already cover a lot of ground, but you can register a custom
formatter when you need one:

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
handlers usually only provide punctuation and child items.

## 🛠️ Development

```bash
mise run lint
mise run docs:build
nox
```

## 📚 Learn More

- [Project guide](docs/README.md)
- [Custom formatter guide](docs/guides/custom-formatters.md)
- [Published API reference](https://liblaf.github.io/pretty/)
