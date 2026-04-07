from typing import Any

from rich.console import Console

from liblaf.pretty._describe import DescribeContext
from liblaf.pretty._lower import LoweredContainer
from liblaf.pretty._spec import SpecNode, TraceContext
from liblaf.pretty._trace import LowerContext, TracedContainer, TracedRef


def test_recursive_container_keeps_traced_items() -> None:
    obj: list[Any] = [1, 2, 3]
    obj.append(obj)

    describe_ctx = DescribeContext()
    spec: SpecNode = describe_ctx.describe(obj)
    trace_ctx: TraceContext = describe_ctx.finish()
    traced = trace_ctx.trace(spec)

    assert isinstance(traced, TracedContainer)
    assert len(traced.items) == 4
    assert isinstance(traced.items[-1].value, TracedRef)

    lower_ctx: LowerContext = trace_ctx.finish()
    lowered = traced.lower(lower_ctx)
    assert isinstance(lowered, LoweredContainer)
    console = Console(width=120, record=True)
    with console.capture() as capture:
        console.print(lowered, end="")
    assert capture.get() == f"[1, 2, 3, <list @ {id(obj):x}>]  # <list @ {id(obj):x}>"
