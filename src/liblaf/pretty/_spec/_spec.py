import abc

import attrs

from liblaf.pretty._trace import Traced

from ._context import TraceContext


@attrs.frozen
class Spec(abc.ABC):
    cls: type = attrs.field(kw_only=True)
    id_: int = attrs.field(kw_only=True)
    referenceable: bool = attrs.field(default=True, kw_only=True)

    @abc.abstractmethod
    def trace(self, ctx: TraceContext) -> Traced: ...
