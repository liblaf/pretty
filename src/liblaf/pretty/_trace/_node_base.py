import abc
from typing import override

import attrs

from liblaf.pretty._lower import LoweredNode

from ._base import Traced
from ._context import LowerContext


@attrs.define
class TracedNode(Traced):
    @override
    @abc.abstractmethod
    def lower(self, ctx: LowerContext) -> LoweredNode: ...
