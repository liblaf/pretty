import abc
from typing import Any, Self, override

import attrs
from rich.text import Text

from liblaf.pretty._compile import Lowered, LoweredLeaf

from ._base import LowerContext, Traced


@attrs.define
class TracedReference(Traced):
    cls: type
    obj_id: int

    @classmethod
    def new(cls, obj: Any) -> Self:
        return cls(cls=type(obj), obj_id=id(obj))

    @override
    def lower(self, ctx: LowerContext) -> Lowered:
        return LoweredLeaf(ctx.make_ref_text(self.cls, self.obj_id))


@attrs.define
class TracedReferent(Traced):
    cls: type = attrs.field(kw_only=True)
    obj_id: int = attrs.field(kw_only=True)

    @override
    def lower(self, ctx: LowerContext) -> Lowered:
        lowered: Lowered = self.lower_referent(ctx)
        if ctx.obj_id_counter[self.obj_id] > 1:
            lowered.annotation = Text.assemble(
                "  # ", ctx.make_ref_text(self.cls, self.obj_id).plain, style="dim"
            )
        return lowered

    @abc.abstractmethod
    def lower_referent(self, ctx: LowerContext) -> Lowered:
        raise NotImplementedError
