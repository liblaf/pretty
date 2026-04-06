from collections.abc import Iterable

import attrs
from rich.text import Text

from liblaf.pretty._const import INDENT
from liblaf.pretty._trace import (
    TRACED_ELLIPSIS,
    Traced,
    TracedContainer,
    TracedItem,
    TracedItemValue,
    TracedLeaf,
)

from ._context import TraceContext
from ._item import SpecItem
from ._spec import Spec


@attrs.frozen
class SpecContainer(Spec):
    begin: Text
    items: Iterable[SpecItem]
    end: Text

    def _default_empty(self) -> Text:
        return self.begin[0] + self.end[-1]

    empty: Text = attrs.field(
        default=attrs.Factory(_default_empty, takes_self=True), kw_only=True
    )
    indent: Text = attrs.field(default=INDENT, kw_only=True)

    def trace(self, ctx: TraceContext) -> Traced:
        # TODO: return TracedRef if this should be a reference
        anchor: bool = ctx.id_counter[self.id_] > 1
        if not self.items:
            return TracedLeaf(
                cls=self.cls, id_=self.id_, value=self.empty, anchor=anchor
            )
        if ctx.depth >= ctx.options.max_level:
            items: list[TracedItem] = [TracedItemValue(TRACED_ELLIPSIS)]
        else:
            items: list[TracedItem] = []
            for item in self.items:
                if len(items) >= ctx.options.max_list:
                    items.append(TracedItemValue(TRACED_ELLIPSIS))
                    break
                items.append(item.trace(ctx))
        return TracedContainer(
            cls=self.cls,
            id_=self.id_,
            begin=self.begin,
            end=self.end,
            items=items,
            indent=self.indent,
            anchor=anchor,
        )
