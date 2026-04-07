from rich.text import Text

from liblaf.pretty._describe import DescribeContext, describe
from liblaf.pretty._spec import SpecContainer, SpecItem, SpecNode, SpecValueItem
from liblaf.pretty._trace import Ref


@describe.register_type(list)
def _describe_list(obj: list, ctx: DescribeContext, depth: int) -> SpecContainer:
    if depth < ctx.options.max_level:
        items: list[SpecItem] = [
            ctx.describe_value_item(item) for item in ctx.truncate_list(obj)
        ]
        items: list[SpecItem] = ctx.add_separators(items)
    else:
        items: list[SpecItem] = [SpecValueItem.ellipsis()]
    return SpecContainer(
        begin=Text("["),
        items=items,
        end=Text("]"),
        indent=ctx.options.indent,
        ref=Ref.from_obj(obj),
        referencable=True,
    )
