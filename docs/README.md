# Pretty

`liblaf.pretty` gives you repr-like output that stays readable when values get
large, nested, shared, or cyclic. It builds a Rich renderable first, then lets
you print it normally or capture width-aware plain text for logs, tests, and
debug output.

## Start Here

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

If you already have a Rich console and just want to print, call `pprint()` or
its alias `pp()` instead.

## How To Use It

`pformat(obj, **kwargs)`
: Return a Rich renderable for `obj`. The returned value also exposes
  `.to_plain(console=...)` for deterministic plain-text captures.

`pprint(obj, **kwargs)`
: Format the object and print it to the active Rich console.

`DescribeContext` and `describe`
: Advanced extension points for projects that want to participate in the
  describe/trace/lower pipeline directly.

## Supported Behaviors

- Builtin containers render with width-aware line breaking.
- Large collections and long scalar reprs truncate according to configurable
  limits.
- `attrs` and `fieldz` objects honor `repr=False` and can hide default-valued
  fields.
- `__rich_repr__` is supported.
- Shared references and cycles are annotated instead of recursing forever.
- `__pretty__(ctx, depth)` can supply custom specs for advanced integrations.

## Formatting Options

The public formatting functions accept keyword arguments with these defaults:

| Keyword | Default | Meaning |
| --- | --- | --- |
| `max_level` | `6` | Maximum nesting depth before values collapse to `...`. |
| `max_list` | `6` | Maximum visible items in list-like containers. |
| `max_array` | `5` | Maximum array items forwarded to repr-style handlers. |
| `max_dict` | `4` | Maximum visible key-value pairs in dictionaries. |
| `max_string` | `30` | Maximum string repr length before truncation. |
| `max_long` | `40` | Maximum integer repr length before truncation. |
| `max_other` | `30` | Maximum repr length for other scalar values. |
| `indent` | `"|   "` | Indentation inserted for broken layouts. |
| `hide_defaults` | `True` | Hide default-valued fields from attrs and rich repr output. |

Explicit kwargs override the environment-backed defaults loaded from `PRETTY_*`
variables.

Width is controlled when you render the result through `Console(width=...)`, so
plain-text output and terminal output can share the same formatted structure.

## Notes For Extenders

The package exports `DescribeContext` and the shared `describe` registry because
the describe stage is extensible. Those names are lower-level than the formatting
functions, and the spec-building helpers currently live in internal modules
rather than the top-level package.

See [API Reference](reference/README.md) for signatures and docstrings.
