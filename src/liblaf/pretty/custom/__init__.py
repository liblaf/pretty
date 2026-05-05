"""Customization helpers for teaching `liblaf.pretty` new formatting rules.

Import [`PrettyContext`][liblaf.pretty.custom.PrettyContext] together with
[`register_type`][liblaf.pretty.custom.register_type],
[`register_func`][liblaf.pretty.custom.register_func], or
[`register_lazy`][liblaf.pretty.custom.register_lazy] when you want to format a
new kind of object. Importing this module also loads the built-in handlers for
core containers, optional array summaries, `fieldz`-compatible models, and
`__rich_repr__` objects.
"""

from ._context import PrettyContext

# register prelude handlers
from ._prelude import _array, _container, _fieldz, _scalar  # noqa: F401
from ._registry import (
    PrettyHandler,
    PrettyRegistry,
    register_func,
    register_lazy,
    register_type,
    registry,
)

__all__ = [
    "PrettyContext",
    "PrettyHandler",
    "PrettyRegistry",
    "register_func",
    "register_lazy",
    "register_type",
    "registry",
]
