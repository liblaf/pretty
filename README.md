# Pretty

`liblaf.pretty` pretty-prints Python objects as repr-like, width-aware Rich
renderables.

[Guide](docs/README.md) ·
[Custom Formatters](docs/guides/custom-formatters.md) ·
[API Reference](https://liblaf.github.io/pretty/) ·
[Changelog](CHANGELOG.md)

## Install

```bash
uv add liblaf-pretty
# or
pip install liblaf-pretty
```

## Quick Start

Use `pformat()` when you want a Rich renderable that can be printed directly or
converted into stable plain text for logs, tests, and snapshots:

```python
from rich.console import Console

from liblaf.pretty import pformat

rendered = pformat({"alpha": [1, 2, 3]})
console = Console(
    width=12,
    color_system=None,
    soft_wrap=True,
    no_color=True,
    markup=False,
    emoji=False,
    highlight=False,
)

print(rendered.to_plain(console=console), end="")
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

## Built In

- builtin containers such as `dict`, `list`, `tuple`, `set`, and `frozenset`
- `fieldz`-compatible models, including common `attrs` patterns
- objects with `__rich_repr__`
- shared and cyclic references
- per-call overrides layered on top of `PRETTY_*` defaults

## Configuration

The public formatting helpers accept these keyword overrides:

- `max_level`, `max_list`, `max_array`, `max_dict`
- `max_string`, `max_long`, `max_other`
- `indent`
- `hide_defaults`

Those values can also come from environment variables:

```bash
export PRETTY_MAX_LIST=2
export PRETTY_INDENT='[bold]>>[/] '
```

`indent` accepts plain text, Rich markup, ANSI-colored strings, or
`rich.text.Text`.

## Reference Tracking

Referencable objects such as mappings, sets, frozensets, and custom containers
can be annotated when the same object appears more than once:

```python
from rich.console import Console

from liblaf.pretty import pformat

shared = {"x": 1}
rendered = pformat({"left": shared, "right": shared})
console = Console(width=80, color_system=None, soft_wrap=True)

print(rendered.to_plain(console=console), end="")
```

```text
{
|   'left': {'x': 1},  # <dict @ 7f...>
|   'right': <dict @ 7f...>
}
```

Lists and tuples still render safely, but repeated appearances keep rendering
their value instead of collapsing into a shared-reference tag.

## Custom Formatting

You can extend the formatter in four main ways:

- implement `__pretty__(self, ctx)` when you own the class
- use `register_type()` for one concrete type and its subclasses
- use `register_func()` for structural matching
- use `register_lazy()` for optional dependencies that should only activate
  after their module is already imported

For a practical walkthrough, see [Custom Formatters](docs/guides/custom-formatters.md).

## Development

```bash
mise run lint
mise run docs:build
nox
```
