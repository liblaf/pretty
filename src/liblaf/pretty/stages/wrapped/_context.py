"""Traversal state for wrapped nodes."""

import attrs

from liblaf.pretty._config import PrettyOptions, config
from liblaf.pretty.stages.traced import LowerContext, TracedObject

from ._typename import disambiguate_typenames


@attrs.define
class TraceContext:
    """Mutable state used while resolving wrapped nodes into traced nodes."""

    depth: int = 0
    options: PrettyOptions = attrs.field(factory=config.dump)
    trace_cache: dict[int, TracedObject] = attrs.field(factory=dict)
    types: set[type] = attrs.field(factory=set)

    def finish(self) -> LowerContext:
        """Freeze the traced type information into a lowering context."""
        return LowerContext(typenames=disambiguate_typenames(self.types))
