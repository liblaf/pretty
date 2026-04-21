
from typing import Any, Unpack

import rich
from rich.console import Console

from liblaf.pretty.custom import PrettyContext
from liblaf.pretty.stages.lowered import LoweredNode
from liblaf.pretty.stages.traced import LowerContext, TracedNode
from liblaf.pretty.stages.wrapped import WrappedNode

from ._config import PrettyOptions, PrettyOverrides, config


def pformat(obj: Any, **kwargs: Unpack[PrettyOverrides]) -> LoweredNode:
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
    if console is None:
        console: Console = rich.get_console()
    lowered: LoweredNode = pformat(obj, **kwargs)
    console.print(lowered)


pp = pprint
