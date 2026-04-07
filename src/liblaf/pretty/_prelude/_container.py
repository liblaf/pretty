from typing import Any

from rich.text import Text

from liblaf.pretty._const import COMMA
from liblaf.pretty._describe import DescribeContext, describe
from liblaf.pretty._spec import SpecContainer, SpecItem


@describe.register_type(dict)
def _describe_dict(
    obj: dict[Any, Any], ctx: DescribeContext, depth: int
) -> SpecContainer:
    if depth < ctx.options.max_level:
        items: list[SpecItem] = [
            ctx.describe_dict_item(key, value)
            for key, value in ctx.truncate_dict(obj.items())
        ]
        items: list[SpecItem] = ctx.add_separators(items)
    else:
        items: list[SpecItem] = [ctx.ellipsis()]
    return SpecContainer(
        begin=Text("{", "brace"),
        items=items,
        end=Text("}", "brace"),
        indent=ctx.options.indent,
        ref=ctx.ref(obj),
        referencable=True,
    )


@describe.register_type(frozenset)
def _describe_frozenset(
    obj: frozenset[Any], ctx: DescribeContext, depth: int
) -> SpecContainer:
    if depth < ctx.options.max_level:
        items: list[SpecItem] = [
            ctx.describe_value_item(item) for item in ctx.truncate_list(obj)
        ]
        items: list[SpecItem] = ctx.add_separators(items)
    else:
        items: list[SpecItem] = [ctx.ellipsis()]
    return SpecContainer(
        begin=Text("({", "brace"),
        items=items,
        end=Text("})", "brace"),
        indent=ctx.options.indent,
        ref=ctx.ref(obj),
        referencable=True,
        empty=Text("()", "brace"),
    )


@describe.register_type(list)
def _describe_list(obj: list, ctx: DescribeContext, depth: int) -> SpecContainer:
    if depth < ctx.options.max_level:
        items: list[SpecItem] = [
            ctx.describe_value_item(item) for item in ctx.truncate_list(obj)
        ]
        items: list[SpecItem] = ctx.add_separators(items)
    else:
        items: list[SpecItem] = [ctx.ellipsis()]
    return SpecContainer(
        begin=Text("[", "brace"),
        items=items,
        end=Text("]", "brace"),
        indent=ctx.options.indent,
        ref=ctx.ref(obj),
        referencable=True,
    )


@describe.register_type(set)
def _describe_set(obj: set[Any], ctx: DescribeContext, depth: int) -> SpecContainer:
    if depth < ctx.options.max_level:
        items: list[SpecItem] = [
            ctx.describe_value_item(item) for item in ctx.truncate_list(obj)
        ]
        items: list[SpecItem] = ctx.add_separators(items)
    else:
        items: list[SpecItem] = [ctx.ellipsis()]
    return SpecContainer(
        begin=Text("{", "brace"),
        items=items,
        end=Text("}", "brace"),
        indent=ctx.options.indent,
        ref=ctx.ref(obj),
        referencable=True,
        empty=Text.assemble(("set", "repr.tag_name"), ("()", "brace")),
    )


@describe.register_type(tuple)
def _describe_tuple(obj: tuple, ctx: DescribeContext, depth: int) -> SpecContainer:
    if depth < ctx.options.max_level:
        items: list[SpecItem] = [
            ctx.describe_value_item(item) for item in ctx.truncate_list(obj)
        ]
        items: list[SpecItem] = ctx.add_separators(items)
        if len(obj) == 1:
            items[0].suffix += COMMA
    else:
        items: list[SpecItem] = [ctx.ellipsis()]
    return SpecContainer(
        begin=Text("(", "brace"),
        items=items,
        end=Text(")", "brace"),
        indent=ctx.options.indent,
        ref=ctx.ref(obj),
        referencable=True,
    )
