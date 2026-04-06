import abc
from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._const import EMPTY
from liblaf.pretty._lower import LoweredObject

from ._context import LowerContext
from ._id import TraceId
from ._traced import Traced


@attrs.define
class TracedObject(Traced):
    ref: TraceId | None = attrs.field(default=None, kw_only=True)
    annotation: bool = attrs.field(default=False, kw_only=True)

    @override
    @abc.abstractmethod
    def lower(self, ctx: LowerContext) -> LoweredObject: ...

    def make_annotation(self, ctx: LowerContext) -> Text:
        if self.ref is None:
            return EMPTY
        typename: str = ctx.get_ref_typename(self.ref.cls)
        return Text(f"  # <{typename} @ {self.ref.id_:x}>", "dim")
