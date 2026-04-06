import attrs

from liblaf.pretty._trace import TracedObject, TracedRef, TraceId

from ._spec import Spec


@attrs.define
class SpecObject[T: TracedObject | TracedRef](Spec[T]):
    ref: TraceId | None = attrs.field(default=None, kw_only=True)
