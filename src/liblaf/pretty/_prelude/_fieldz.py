import contextlib
from collections.abc import Callable, Sequence
from typing import Any

import fieldz
from rich.repr import RichReprResult
from rich.text import Text

from liblaf.pretty._describe import DescribeContext, describe
from liblaf.pretty._spec import SpecContainer, SpecItem, SpecNode


@describe.register_func
def _describe_fieldz(obj: object, ctx: DescribeContext, depth: int) -> SpecNode | None:
    try:
        fields: Sequence[fieldz.Field] = fieldz.fields(obj)
    except TypeError:
        return None
    if depth < ctx.options.max_level:
        items: list[SpecItem] = []
        for field in fields:
            if not field.repr:
                continue
            value: Any = getattr(obj, field.name, fieldz.Field.MISSING)
            if ctx.options.hide_defaults and _safe_equal(value, field.default):
                continue
            items.append(ctx.describe_named_item(field.name, value))
        items: list[SpecItem] = ctx.add_separators(items)
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


@describe.register_func
def _describe_rich_repr(obj: Any, ctx: DescribeContext, depth: int) -> SpecNode | None:
    rich_repr: Callable[[], RichReprResult | None] | None = getattr(
        obj, "__rich_repr__", None
    )
    if rich_repr is None:
        return None
    result: RichReprResult | None = rich_repr()
    if result is None:
        return None
    if depth < ctx.options.max_level:
        items: list[SpecItem] = []
        for item in result:
            match item:
                case (name, value, default):
                    if ctx.options.hide_defaults and _safe_equal(value, default):
                        continue
                    items.append(ctx.describe_named_item(name, value))
                case (name, value):
                    items.append(ctx.describe_named_item(name, value))
                case (value,):
                    items.append(ctx.describe_value_item(value))
                case value:
                    items.append(ctx.describe_value_item(value))
        items: list[SpecItem] = ctx.add_separators(items)
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


def _safe_equal(a: Any, b: Any) -> bool:
    if a is b:
        return True
    with contextlib.suppress(Exception):
        return a == b
    return False
