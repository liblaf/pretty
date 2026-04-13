import attrs
from rich.text import Text

from liblaf.pretty.literals import EMPTY

from ._context import LowerContext
from ._identifier import ObjectIdentifier
from ._node_base import TracedNode


@attrs.define
class TracedObject(TracedNode):
    has_ref: bool = attrs.field(default=False, kw_only=True)
    identifier: ObjectIdentifier = attrs.field(kw_only=True)

    def make_annotation(self, ctx: LowerContext) -> Text:
        if not self.has_ref:
            return EMPTY
        typename: str = ctx.get_ref_typename(self.identifier.cls)
        return Text(f"  # <{typename} @ {self.identifier.id_:x}>", "dim")
