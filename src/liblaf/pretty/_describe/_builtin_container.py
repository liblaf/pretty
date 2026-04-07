from typing import Any

from rich.text import Text

from liblaf.pretty._spec import (
    SpecContainer,
    SpecItem,
    SpecLeaf,
    SpecNode,
    SpecValueItem,
)
from liblaf.pretty._trace import Ref

from ._context import DescribeContext
from ._registry import describe
from ._utils import add_separators, truncate


@describe.register_type(list)
def _describe_list(obj: list[Any], ctx: DescribeContext, depth: int) -> SpecContainer:
    if depth < ctx.options.max_level:
        items: list[SpecItem] = []
        for item in truncate(obj, ctx.options.max_list, fill=...):
            spec: SpecNode = ctx.describe(item)
            items.append(SpecValueItem(spec))
        items: list[SpecItem] = add_separators(items)
    else:
        items: list[SpecItem] = [SpecValueItem.ellipsis()]
    spec = SpecContainer(
        begin=Text("["),
        items=items,
        end=Text("]"),
        indent=ctx.options.indent,
        ref=Ref.from_obj(obj),
        referencable=True,
    )
    return spec


@describe.register_type(int)
def _describe_int(obj: int, ctx: DescribeContext, depth: int) -> SpecNode:
    return SpecLeaf(Text(str(obj)), ref=Ref.from_obj(obj), referencable=False)
