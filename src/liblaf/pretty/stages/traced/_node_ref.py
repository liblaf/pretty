"""Reference nodes emitted for repeated referencable objects."""

from typing import override

import attrs
from rich.text import Text

from liblaf.pretty.common import ObjectIdentifier
from liblaf.pretty.stages.lowered import LoweredLeaf

from ._context import LowerContext
from ._node_base import TracedNode


@attrs.define
class TracedRef(TracedNode):
    """Traced node that lowers into a `<Type @ hexid>` reference tag."""

    identifier: ObjectIdentifier

    @override
    def lower(self, ctx: LowerContext) -> LoweredLeaf:
        assert self.identifier.cls is not None
        typename: str = ctx.get_ref_typename(self.identifier.cls)
        return LoweredLeaf(
            Text.assemble(
                ("<", "repr.tag_start"),
                (typename, "repr.tag_name"),
                (f" @ {self.identifier.id_:x}", "repr.tag_contents"),
                (">", "repr.tag_end"),
            )
        )
