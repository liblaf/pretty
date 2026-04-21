"""Fallback repr-based formatting helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rich.highlighter import ReprHighlighter
from rich.text import Text

from liblaf.pretty.stages.wrapped import WrappedLeaf

if TYPE_CHECKING:
    from ._context import PrettyContext

_HIGHLIGHTER: ReprHighlighter = ReprHighlighter()


def pretty_repr(
    obj: Any, ctx: PrettyContext, *, referencable: bool = True
) -> WrappedLeaf:
    """Format `obj` with `reprlib` and Rich's repr highlighter."""
    raw: str = ctx.arepr.repr1(obj, ctx.arepr.maxlevel - ctx.depth)
    text: Text = _HIGHLIGHTER(raw)
    return ctx.leaf(obj, text, referencable=referencable)
