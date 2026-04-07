# Pretty

`liblaf.pretty` formats Python objects into Rich renderables with width-aware
layout, repr-style truncation, and stable shared-reference tracking.

## Quick Start

Use `pformat()` when you want a renderable object that can be printed through
Rich or captured as deterministic plain text:

```python
from rich.console import Console

from liblaf.pretty import pformat

rendered = pformat({"alpha": [1, 2, 3]})
console = Console(width=12, color_system=None, soft_wrap=True)

print(rendered.to_plain(console))
```

```text
{
|   'alpha': [
|   |   1,
|   |   2, 3
|   ]
}
```

Use `pprint()` or `pp()` when you want to send the formatted object directly to
the active Rich console:

```python
from liblaf.pretty import pprint

pprint({"alpha": [1, 2, 3]}, max_list=3)
```

## What It Handles

- Builtin containers such as `dict`, `list`, `tuple`, `set`, and `frozenset`
- Repr-style truncation for deep, long, or large values
- `attrs` and `fieldz` objects, including `repr=False` fields and hidden defaults
- Objects with `__rich_repr__`
- Shared and cyclic references
- Advanced `__pretty__(ctx, depth)` hooks

## Formatting Knobs

The top-level formatters accept keyword arguments, not a `PrettyOptions`
instance:

- `max_level`, `max_list`, `max_array`, `max_dict`
- `max_string`, `max_long`, `max_other`
- `indent`
- `hide_defaults`

Explicit keyword arguments override the environment-backed defaults loaded from
`PRETTY_*` variables.

Width is chosen when you render the result through a Rich `Console`, not when
you call `pformat()`.

## Public Surface

The top-level package exports:

```python
from liblaf.pretty import DescribeContext, describe, pformat, pp, pprint
```

`DescribeContext` and the shared `describe` registry are advanced extension
points. Most callers only need `pformat()` or `pprint()`.

For a longer guide, see [`docs/README.md`](docs/README.md). For signatures and
docstrings, see [`docs/reference/README.md`](docs/reference/README.md).
