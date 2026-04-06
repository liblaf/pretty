import abc

import attrs

from liblaf.pretty._lower import Lowered

from ._context import LowerContext


@attrs.frozen
class Traced(abc.ABC):
    cls: type
    id_: int

    @abc.abstractmethod
    def lower(self, ctx: LowerContext) -> Lowered: ...
