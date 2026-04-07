from __future__ import annotations

import reprlib
from typing import TYPE_CHECKING

from rich.highlighter import ReprHighlighter
from rich.text import Text

from liblaf.pretty._spec import SpecLeaf, SpecNode
from liblaf.pretty._trace import Ref
from liblaf.pretty._utils import has_ansi

if TYPE_CHECKING:
    from ._context import DescribeContext

_HIGHLIGHTER: ReprHighlighter = ReprHighlighter()


def describe_repr(
    obj: object, ctx: DescribeContext, depth: int, *, referencable: bool = True
) -> SpecNode:
    arepr = reprlib.Repr(
        maxlevel=ctx.options.max_level,
        maxtuple=ctx.options.max_list,
        maxlist=ctx.options.max_list,
        maxarray=ctx.options.max_array,
        maxdict=ctx.options.max_dict,
        maxset=ctx.options.max_list,
        maxfrozenset=ctx.options.max_list,
        maxdeque=ctx.options.max_list,
        maxstring=ctx.options.max_string,
        maxlong=ctx.options.max_long,
        maxother=ctx.options.max_other,
        indent=ctx.options.indent.plain,
    )
    raw: str = arepr.repr1(obj, level=ctx.options.max_level - depth)
    if has_ansi(raw):
        text: Text = Text.from_ansi(raw)
    else:
        text: Text = _HIGHLIGHTER(raw)
    return SpecLeaf(text, ref=Ref.from_obj(obj), referencable=referencable)
