import types
from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._const import ELLIPSIS
from liblaf.pretty._trace import Traced, TracedLeaf

from ._context import TraceContext
from ._spec import Spec


@attrs.frozen
class SpecLeaf(Spec):
    value: Text
    referenceable: bool = attrs.field(default=False, kw_only=True)

    @override
    def trace(self, ctx: TraceContext) -> Traced:
        # TODO: return TracedRef if this should be a reference
        return TracedLeaf(
            cls=self.cls,
            id_=self.id_,
            value=self.value,
            anchor=ctx.id_counter[self.id_] > 1,
        )


SPEC_ELLIPSIS = SpecLeaf(
    ELLIPSIS, cls=types.EllipsisType, id_=id(...), referenceable=False
)
