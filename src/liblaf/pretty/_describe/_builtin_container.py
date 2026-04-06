from collections.abc import Generator
from typing import Any

from rich.text import Text

from liblaf.pretty._spec import SpecContainer, SpecItem, SpecItemValue, SpecObject
from liblaf.pretty._trace import TraceId

from ._context import DescribeContext
from ._utils import add_separators, truncate


def _describe_list(obj: list[Any], ctx: DescribeContext) -> SpecContainer:
    def lazy_items() -> Generator[SpecItem]:
        items: list[SpecItem] = []
        for item in truncate(obj, ctx.options.max_list, fill=...):
            spec: SpecObject = ctx.describe(item)
            items.append(SpecItemValue(spec))
        items: list[SpecItem] = add_separators(items)
        yield from items

    spec = SpecContainer(
        begin=Text("["), items=lazy_items(), end=Text("]"), ref=TraceId.from_obj(obj)
    )
    return spec
