from typing import Any, Unpack

import rich
from rich.console import Console

from ._compile import Lowered
from ._config import PrettyOptions, config
from ._lower import LowerContext, Traced
from ._trace import TraceContext, trace


def pdoc(
    obj: Any, console: Console | None = None, **kwargs: Unpack[PrettyOptions]
) -> Lowered:
    console: Console = _get_console(console, **kwargs)
    trace_ctx: TraceContext = TraceContext.from_options(**kwargs)
    traced: Traced = trace(obj, trace_ctx)
    lower_ctx: LowerContext = trace_ctx.lower()
    return traced.lower(lower_ctx)


def pformat(
    obj: Any,
    console: Console | None = None,
    *,
    soft_wrap: bool = True,
    **kwargs: Unpack[PrettyOptions],
) -> str:
    console: Console = _get_console(console, **kwargs)
    lowered: Lowered = pdoc(obj, console=console, **kwargs)
    with console.capture() as capture:
        console.print(lowered, soft_wrap=soft_wrap)
    return capture.get()


def pprint(
    obj: Any,
    console: Console | None = None,
    *,
    soft_wrap: bool = True,
    **kwargs: Unpack[PrettyOptions],
) -> None:
    if console is None:
        console: Console = rich.get_console()
    lowered: Lowered = pdoc(obj, console=console, **kwargs)
    console.print(lowered, soft_wrap=soft_wrap)


def _get_console(console: Console | None, **kwargs: Unpack[PrettyOptions]) -> Console:
    if console is not None:
        return console
    width: int | None = kwargs.get("max_width")
    if width is None:
        width: int = config.max_width.get()
    return Console(color_system=None, soft_wrap=True, width=width)
