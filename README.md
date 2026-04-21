# Pretty

`liblaf.pretty` pretty-prints Python objects as Rich renderables. It keeps
repr-like syntax, chooses line breaks at render time, truncates large values,
and exposes a small extension surface for custom formatting rules.

## Install

```bash
uv add liblaf-pretty
# or
pip install liblaf-pretty
```

## Quick Start

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

If you already have a Rich console, `pprint()` and `pp()` format and print in
one step:

```python
from liblaf.pretty import pprint

pprint({"alpha": [1, 2, 3]}, max_list=3)
```

## Why `liblaf.pretty`

- Width-aware layout is chosen by Rich when the renderable is printed.
- Deep, wide, or long values are truncated with repr-style ellipses.
- `attrs`, `fieldz`, and `__rich_repr__` objects work out of the box.
- Shared references are annotated for referencable containers and custom
  objects, while cyclic values still render safely.
- Custom hooks are available through `__pretty__()`, `register_type()`,
  `register_func()`, and `register_lazy()`.

## Configuration

The public formatters accept per-call overrides for:

- `max_level`, `max_list`, `max_array`, `max_dict`
- `max_string`, `max_long`, `max_other`
- `indent`
- `hide_defaults`

Those overrides sit on top of environment-backed defaults loaded from
`PRETTY_*` variables. Width is still chosen later, when Rich renders the result
through a `Console`.

## Custom Formatting

Use `register_type()` when you want one concrete class to render in a specific
way:

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

The longer guide lives in [`docs/README.md`](docs/README.md), with a focused
extension guide at [`docs/guides/custom-formatters.md`](docs/guides/custom-formatters.md).

## Development

```bash
mise run lint
mise run docs:build
nox
```
