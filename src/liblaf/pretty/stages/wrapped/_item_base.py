import abc
from collections.abc import Iterable
from typing import override

import attrs
from rich.text import Text

from liblaf.pretty.literals import EMPTY
from liblaf.pretty.stages.traced import TracedItem

from ._base import Wrapped, WrappedChild
from ._context import TraceContext


@attrs.define
class WrappedItem(Wrapped):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @override
    @abc.abstractmethod
    def trace(self, ctx: TraceContext) -> tuple[Iterable[WrappedChild], TracedItem]: ...
