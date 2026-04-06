from collections.abc import Generator
from typing import Any

from rich.text import Text

from liblaf.pretty._const import COMMA
from liblaf.pretty._spec import Spec, SpecContainer, SpecItem, SpecItemValue
from liblaf.pretty._trace import TraceId

from ._context import DescribeContext


def _describe_list(obj: list[Any], ctx: DescribeContext) -> Spec:
    def lazy_items() -> Generator[SpecItem]:
        if ctx.depth > ctx.options.max_depth:
            items: list[SpecItem] = [...]
        else:
            items: list[SpecItem] = []
            for item in obj:
                if len(items) > ctx.options.max_list:
                    items.append(...)
                    break
                items.append(SpecItemValue(ctx.describe(item)))
        for i, item in enumerate(items):
            if i > 0:
                item.prefix = COMMA
            if i < len(items) - 1:
                item.suffix = COMMA
        yield from items

    spec = SpecContainer(
        begin=Text("["), items=lazy_items(), end=Text("]"), ref=TraceId.from_obj(obj)
    )
    return spec
