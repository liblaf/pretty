"""Public formatting helpers."""

from typing import Any, Unpack

import rich
from rich.console import Console

from liblaf.pretty.custom import PrettyContext
from liblaf.pretty.stages.lowered import LoweredNode
from liblaf.pretty.stages.traced import LowerContext, TracedNode
from liblaf.pretty.stages.wrapped import WrappedNode

from ._config import PrettyOptions, PrettyOverrides, config


def pformat(obj: Any, **kwargs: Unpack[PrettyOverrides]) -> LoweredNode:
    """Format an object into a width-aware Rich renderable.

    The returned value can be passed to `Console.print()` or converted into
    deterministic plain text with
    [`Lowered.to_plain`][liblaf.pretty.stages.lowered.Lowered.to_plain].

    Args:
        obj: Object to format.
        **kwargs: Formatting overrides merged over the environment-backed
            defaults loaded from `PRETTY_*` variables.

    Returns:
        A lowered renderable node for the formatted object.

    Examples:
        ```python
        from liblaf.pretty import pformat

        print(pformat([1, 2, 3], max_list=1).to_plain(), end="")
        ```
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
    """Print a formatted object to a Rich console.

    Args:
        obj: Object to format and print.
        console: Console to print to. When omitted, use
            [`rich.get_console`][].
        **kwargs: Formatting overrides forwarded to [liblaf.pretty.pformat][].
    """
    if console is None:
        console: Console = rich.get_console()
    lowered: LoweredNode = pformat(obj, **kwargs)
    console.print(lowered)


pp = pprint
