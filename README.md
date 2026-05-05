<div align="center" markdown>

![Pretty](https://socialify.git.ci/liblaf/pretty/image?description=1&forks=1&issues=1&language=1&name=1&owner=1&pattern=Transparent&pulls=1&stargazers=1&theme=Auto)

**[Explore the docs »](https://liblaf.github.io/pretty/)**

[![Codecov](https://codecov.io/gh/liblaf/pretty/graph/badge.svg)](https://codecov.io/gh/liblaf/pretty)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/liblaf-pretty?logo=python&logoColor=white)](https://pypi.org/project/liblaf-pretty/)
[![PyPI - Types](https://img.shields.io/pypi/types/liblaf-pretty?logo=python&logoColor=white)](https://pypi.org/project/liblaf-pretty/)
[![PyPI Version](https://img.shields.io/pypi/v/liblaf-pretty?logo=pypi&logoColor=white)](https://pypi.org/project/liblaf-pretty/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[API Reference](https://liblaf.github.io/pretty/reference/liblaf/pretty/) · [Changelog](https://github.com/liblaf/pretty/blob/main/CHANGELOG.md) · [Report Bug](https://github.com/liblaf/pretty/issues)

![Rule](https://cdn.jsdelivr.net/gh/andreasbm/readme/assets/lines/rainbow.png)

</div>

## ✨ Features

- Plain-text formatting for logs and snapshots, plus a Rich renderable path for
  width-aware console output.
- Built-in handling for common containers, `fieldz`-compatible models, and
  objects with `__rich_repr__`.
- Shared-reference and cycle tracking for referencable objects such as
  mappings, sets, frozensets, and custom containers.
- A small customization surface through `__pretty__()`, `register_type()`,
  `register_func()`, and `register_lazy()`.
- Environment-backed defaults through `PRETTY_*`, with per-call overrides for
  logs, snapshots, tests, and interactive debugging.

## 📦 Installation

```bash
uv add liblaf-pretty
# or
pip install liblaf-pretty
```

## 🧪 Quick Start

Use `pformat()` when you want stable plain text:

```python
from liblaf.pretty import pformat

print(pformat({"alpha": [1, 2, 3]}), end="")
```

```text
{'alpha': [1, 2, 3]}
```

Use `plower()` when you want a Rich renderable whose layout is chosen later by
the target `Console`. If you already have a console, use `pprint()` or its alias
`pp()` for the print-now path.

## 🎛️ Configuration

The public formatting helpers accept per-call overrides for:

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

## 🔁 Shared References

Repeated referencable objects are annotated on first appearance and then render
as `<Type @ hexid>` references later in the output. Lists and tuples stay safe
too, but they repeat their value instead of collapsing into a reference tag.

## 🧩 Custom Formatting

Reach for the smallest hook that matches the job:

- Implement `__pretty__(self, ctx)` when you own the class.
- Use `register_type()` for a concrete type and its subclasses.
- Use `register_func()` for structural matching.
- Use `register_lazy()` for optional dependencies that should only activate
  after their module is already imported.

`PrettyContext` gives custom formatters the builder helpers they usually need:
`ctx.container()`, `ctx.leaf()`, `ctx.positional()`, `ctx.name_value()`, and
`ctx.key_value()`.

For the full walkthrough, see the
[custom formatter guide](https://liblaf.github.io/pretty/guides/custom-formatters/).

## 🛠️ Development

Common workflows:

```bash
mise run lint
mise run docs:build
mise run docs:serve
mise run gen:ref-pages
nox
```

`nox` runs the test matrix across Python `3.12`, `3.13`, and `3.14`, with both
`highest` and `lowest-direct` dependency resolution.

---

#### 📝 License

Copyright © 2026 [liblaf](https://github.com/liblaf). <br />
This project is [MIT](https://spdx.org/licenses/MIT.html) licensed.
