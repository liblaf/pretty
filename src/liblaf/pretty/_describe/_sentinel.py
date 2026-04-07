from __future__ import annotations

from typing import TYPE_CHECKING

from liblaf.pretty._spec import SpecLeaf, SpecNode

if TYPE_CHECKING:
    from ._context import DescribeContext


class _TruncatedType:
    def __repr__(self) -> str:
        return "<TRUNCATED>"

    def __pretty__(self, ctx: DescribeContext, depth: int) -> SpecNode:
        return SpecLeaf.ellipsis()
