import abc

from liblaf.pretty._lower import Lowered

from ._context import LowerContext


class Traced(abc.ABC):
    @abc.abstractmethod
    def lower(self, ctx: LowerContext) -> Lowered: ...
