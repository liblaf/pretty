from __future__ import annotations

import abc
from collections.abc import Iterable
from typing import TYPE_CHECKING, override

import attrs
from rich.text import Text

from liblaf.pretty._trace import TracedItem
from liblaf.pretty.literals import EMPTY

from ._base import Child, Wrapped

if TYPE_CHECKING:
    from ._context import TraceContext


@attrs.define
class WrappedItem(Wrapped):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @override
    @abc.abstractmethod
    def trace(self, ctx: TraceContext) -> tuple[Iterable[Child], TracedItem]: ...
