from typing import Any

from rich.text import Text

from liblaf.pretty._const import COMMA
from liblaf.pretty._spec import (
    SPEC_ITEM_ELLIPSIS,
    Spec,
    SpecContainer,
    SpecItem,
    SpecItemValue,
)

from ._context import DescribeContext


def _describe_list(obj: list[Any], ctx: DescribeContext) -> Spec:
    if ctx.depth > ctx.options.max_depth:
        items: list[SpecItem] = [SPEC_ITEM_ELLIPSIS]
    else:
        items: list[SpecItem] = []
        for item in obj:
            if len(items) > ctx.options.max_list:
                items.append(SPEC_ITEM_ELLIPSIS)
                break
            items.append(SpecItemValue(ctx.describe(item)))
    for i, item in enumerate(items):
        if i > 0:
            item.prefix = COMMA
        if i < len(items) - 1:
            item.suffix = COMMA
    spec = SpecContainer(
        cls=type(obj),
        id_=id(obj),
        begin=Text("["),
        items=items,
        end=Text("]"),
        referenceable=True,
    )
    return spec
