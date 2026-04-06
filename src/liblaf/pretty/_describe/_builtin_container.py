from typing import Any

from rich.text import Text

from liblaf.pretty._const import COMMA
from liblaf.pretty._spec import Spec, SpecContainer, SpecItem, SpecItemValue

from ._context import DescribeContext


def _describe_list(obj: list[Any], ctx: DescribeContext) -> Spec:
    items: list[SpecItem] = [SpecItemValue(ctx.describe(item)) for item in obj]
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
