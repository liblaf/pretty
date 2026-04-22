"""Base class for wrapped nodes."""

import abc
from collections.abc import Iterable
from typing import override

import attrs

from liblaf.pretty.common import ObjectIdentifier
from liblaf.pretty.stages.traced import TracedNode

from ._base import Wrapped, WrappedChild
from ._context import TraceContext


@attrs.define
class WrappedNode(Wrapped):
    """Base wrapped node with a stable object identifier."""

    identifier: ObjectIdentifier = attrs.field(kw_only=True)

    @override
    @abc.abstractmethod
    def trace(self, ctx: TraceContext) -> tuple[Iterable[WrappedChild], TracedNode]: ...
