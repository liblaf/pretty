# Pretty

`liblaf.pretty` formats Python objects as Rich renderables. It keeps repr-like
syntax, decides where to break lines at render time, truncates large values,
and annotates repeated references instead of recursing forever.

## Install

```bash
uv add liblaf-pretty
# or
pip install liblaf-pretty
```

## Quick Start

Use `pformat()` when you want a Rich renderable that can be printed directly or
captured as deterministic plain text:

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

## What It Handles

- Builtin containers such as `dict`, `list`, `tuple`, `set`, and `frozenset`
- Repr-style truncation for deep, wide, or long values
- `attrs` and `fieldz` objects, with default-valued fields hidden by default
- Objects with `__rich_repr__`
- Shared and cyclic references
- Custom handlers via `register_type()`, `register_func()`, `register_lazy()`,
  or `__pretty__(self, ctx)`

## Configuration

The public formatters accept keyword overrides for:

- `max_level`, `max_list`, `max_array`, `max_dict`
- `max_string`, `max_long`, `max_other`
- `indent`
- `hide_defaults`

Those overrides sit on top of environment-backed defaults loaded from
`PRETTY_*` variables. Width is still chosen later, when Rich renders the result
through a `Console`.

## Custom Formatting

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
handlers usually provide only the delimiters.

The longer guide lives in [`docs/README.md`](docs/README.md), with a focused
extension guide at [`docs/guides/custom-formatters.md`](docs/guides/custom-formatters.md).
