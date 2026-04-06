import abc

import attrs

from liblaf.pretty._lower import Lowered

from ._context import LowerContext


@attrs.define
class Traced(abc.ABC):
    @abc.abstractmethod
    def lower(self, ctx: LowerContext) -> Lowered: ...
