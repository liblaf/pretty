import attrs

from liblaf.pretty._config import PrettyOptions, config
from liblaf.pretty.stages.traced import LowerContext, TracedObject

from ._typename import disambiguate_typenames


@attrs.define
class TraceContext:
    depth: int = 0
    options: PrettyOptions = attrs.field(factory=config.dump)
    trace_cache: dict[int, TracedObject] = attrs.field(factory=dict)
    _types: set[type] = attrs.field(factory=set)

    def finish(self) -> LowerContext:
        return LowerContext(typenames=disambiguate_typenames(self._types))
