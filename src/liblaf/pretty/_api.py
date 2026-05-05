"""Top-level formatting helpers.

These functions are the public entry point into the wrapped, traced, and
lowered pipeline that powers `liblaf.pretty`. Use [`pformat`][liblaf.pretty.pformat]
for captured plain text, [`plower`][liblaf.pretty.plower] for a Rich renderable,
and [`pprint`][liblaf.pretty.pprint] for console output.
"""

from typing import Any, Unpack

import rich
from rich.console import Console

from liblaf.pretty.custom import PrettyContext
from liblaf.pretty.stages.lowered import LoweredNode
from liblaf.pretty.stages.traced import LowerContext, TracedNode
from liblaf.pretty.stages.wrapped import WrappedNode

from ._config import PrettyOptions, PrettyOverrides, config


def pformat(obj: Any, **kwargs: Unpack[PrettyOverrides]) -> str:
    """Format `obj` as plain text.

    This helper lowers the object and captures the Rich renderable with a safe
    default console. Use [`plower`][liblaf.pretty.plower] when the final layout
    should depend on a specific Rich console width.

    Args:
        obj: Object to format.
        **kwargs: Per-call overrides merged with [`config`][liblaf.pretty.config].

    Returns:
        Plain-text repr-like output.
    """
    lowered: LoweredNode = plower(obj, **kwargs)
    return lowered.to_plain()


def plower(obj: Any, **kwargs: Unpack[PrettyOverrides]) -> LoweredNode:
    """Build a Rich renderable for `obj`.

    The returned lowered node chooses between flat and broken layouts when Rich
    renders it through a `Console`.

    Args:
        obj: Object to format.
        **kwargs: Per-call overrides merged with [`config`][liblaf.pretty.config].

    Returns:
        A lowered Rich renderable.
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

    This is the side-effecting companion to [`plower`][liblaf.pretty.plower].

    Args:
        obj: Object to format.
        console: Console to render into. When omitted, the active global Rich console
            is used.
        **kwargs: Per-call overrides merged with [`config`][liblaf.pretty.config].
    """
    if console is None:
        console: Console = rich.get_console()
    lowered: LoweredNode = plower(obj, **kwargs)
    console.print(lowered)


pp = pprint
