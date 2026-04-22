"""Top-level formatting helpers.

These functions are the public entry point into the wrapped, traced, and
lowered pipeline that powers `liblaf.pretty`.
"""

from typing import Any, Unpack

import rich
from rich.console import Console

from liblaf.pretty.custom import PrettyContext
from liblaf.pretty.stages.lowered import LoweredNode
from liblaf.pretty.stages.traced import LowerContext, TracedNode
from liblaf.pretty.stages.wrapped import WrappedNode

from ._config import PrettyOptions, PrettyOverrides, config


def pformat(obj: Any, **kwargs: Unpack[PrettyOverrides]) -> LoweredNode:
    """Build a width-aware Rich renderable for `obj`.

    `pformat()` resolves the active configuration, wraps `obj`, traces shared
    and cyclic references, and lowers the result into a Rich renderable. The
    returned object is rendered later by Rich, so the final line breaks still
    depend on the target console width.

    Args:
        obj: Object to format.
        **kwargs: Per-call overrides layered on top of
            [`config`][liblaf.pretty.config].

    Returns:
        A lowered renderable that can be passed to `console.print(...)` or converted
        to deterministic plain text with `to_plain(console=...)`.
    """
    options: PrettyOptions = PrettyOptions(**{**config.to_dict(), **kwargs})
    pretty_ctx: PrettyContext = PrettyContext(options=options)
    wrapped: WrappedNode = pretty_ctx.wrap_lazy(obj)
    traced: TracedNode = pretty_ctx.trace(wrapped)
    lower_ctx: LowerContext = pretty_ctx.finish()
    lowered: LoweredNode = traced.lower(lower_ctx)
    return lowered


def pprint(
    obj: Any, *, console: Console | None = None, **kwargs: Unpack[PrettyOverrides]
) -> None:
    """Format `obj` and print it through a Rich console.

    This is the side-effecting companion to [`pformat`][liblaf.pretty.pformat].

    Args:
        obj: Object to format.
        console: Console to render into. When omitted, the active global Rich console
            is used.
        **kwargs: Per-call overrides forwarded to [`pformat`][liblaf.pretty.pformat].
    """
    if console is None:
        console: Console = rich.get_console()
    lowered: LoweredNode = pformat(obj, **kwargs)
    console.print(lowered)


pp = pprint
