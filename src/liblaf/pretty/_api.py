from typing import Any, Unpack

import rich
from rich.console import Console

from ._conf import PrettyKwargs, PrettyOptions, config
from ._describe import DescribeContext
from ._lower import LoweredNode
from ._spec import SpecNode, TraceContext
from ._trace import LowerContext, TracedNode


def pformat(obj: Any, **kwargs: Unpack[PrettyKwargs]) -> LoweredNode:
    kwargs: PrettyKwargs = {**config.to_dict(), **kwargs}
    describe_ctx: DescribeContext = DescribeContext(options=PrettyOptions(**kwargs))
    spec: SpecNode = describe_ctx.describe(obj)
    trace_ctx: TraceContext = describe_ctx.finish()
    traced: TracedNode = trace_ctx.trace(spec)
    lower_ctx: LowerContext = trace_ctx.finish()
    lowered: LoweredNode = traced.lower(lower_ctx)
    return lowered


def pprint(
    obj: Any, *, console: Console | None = None, **kwargs: Unpack[PrettyKwargs]
) -> None:
    if console is None:
        console: Console = rich.get_console()
    lowered: LoweredNode = pformat(obj, **kwargs)
    console.print(lowered)


pp = pprint
