"""Tracing state shared while wrapped nodes expand into traced nodes."""

import attrs

from liblaf.pretty._config import PrettyOptions, config
from liblaf.pretty.stages.traced import LowerContext, TracedObject

from ._typename import disambiguate_typenames


@attrs.define
class TraceContext:
    """Mutable tracing context with options, caches, and discovered types."""

    depth: int = 0
    options: PrettyOptions = attrs.field(factory=config.dump)
    trace_cache: dict[int, TracedObject] = attrs.field(factory=dict)
    types: set[type] = attrs.field(factory=set)

    def finish(self) -> LowerContext:
        """Build the lowering context with disambiguated type names."""
        return LowerContext(typenames=disambiguate_typenames(self.types))
