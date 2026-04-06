import attrs

from liblaf.pretty._trace import TraceId

from ._spec import Spec


@attrs.define
class SpecObject(Spec):
    ref: TraceId | None = attrs.field(default=None, kw_only=True)
