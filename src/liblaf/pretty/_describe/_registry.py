from __future__ import annotations

import functools
import logging
import sys
import types
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, NamedTuple, Protocol, overload

import attrs

from liblaf.pretty._spec import SpecNode

from ._lazy import LazySpec

if TYPE_CHECKING:
    from _typeshed import IdentityFunction

    from ._context import DescribeContext

logger: logging.Logger = logging.getLogger(__name__)


def _default_type_dispatcher() -> functools._SingleDispatchCallable[SpecNode | None]:
    @functools.singledispatch
    def dispatcher(_obj: object, _ctx: DescribeContext, _depth: int) -> SpecNode | None:
        return None

    return dispatcher


class Handler[T](Protocol):
    def __call__(self, obj: T, ctx: DescribeContext, depth: int) -> SpecNode | None: ...


class LazyType(NamedTuple):
    module: str
    name: str


@attrs.define
class DescribeRegistry:
    _type_dispatcher: functools._SingleDispatchCallable[SpecNode | None] = attrs.field(
        factory=_default_type_dispatcher, init=False
    )
    _handlers: list[Handler] = attrs.field(factory=list, init=False)
    _lazy_handlers: dict[LazyType, Handler] = attrs.field(factory=dict, init=False)

    def __call__(self, obj: object, ctx: DescribeContext) -> SpecNode:
        return self.describe_lazy(obj, ctx)

    def describe_eager(self, obj: object, ctx: DescribeContext, depth: int) -> SpecNode:
        self.resolve_lazy()
        if (
            hasattr(obj, "__pretty__")
            and (spec := obj.__pretty__(ctx, depth)) is not None  # ty:ignore[call-non-callable]
        ):
            return spec
        if (spec := self._type_dispatcher(obj, ctx, depth)) is not None:
            return spec
        for handler in self._handlers:
            if (spec := handler(obj, ctx, depth)) is not None:
                return spec
        raise NotImplementedError

    def describe_lazy(self, obj: object, ctx: DescribeContext) -> SpecNode:
        self.resolve_lazy()
        return LazySpec(ctx, functools.partial(self.describe_eager, obj))

    def register_func[F: Handler](self, func: F) -> F:
        self._handlers.append(func)
        return func

    @overload
    def register_lazy[F: Handler](self, module: str, name: str, func: F) -> F: ...
    @overload
    def register_lazy(
        self, module: str, name: str, func: None = None
    ) -> IdentityFunction: ...
    def register_lazy[F: Handler](
        self, module: str, name: str, func: F | None = None
    ) -> Callable[..., Any]:
        if func is None:
            return functools.partial(self.register_lazy, module, name)
        lazy_type = LazyType(module, name)
        self._lazy_handlers[lazy_type] = func
        return func

    @overload
    def register_type[F: Handler](self, cls: type, func: F) -> F: ...
    @overload
    def register_type[F: Handler](
        self, cls: type, func: None = None
    ) -> IdentityFunction: ...
    def register_type[F: Handler](
        self, cls: type, func: F | None = None
    ) -> Callable[..., Any]:
        return self._type_dispatcher.register(cls, func)

    def resolve_lazy(self) -> None:
        # register prelude handlers
        from . import _builtin_container  # noqa: F401

        for lazy_type, handler in list(self._lazy_handlers.items()):
            module_name, type_name = lazy_type
            if module_name not in sys.modules:
                continue
            module: types.ModuleType = sys.modules[module_name]
            try:
                cls: type = getattr(module, type_name)
            except AttributeError:
                logger.exception("")
                del self._lazy_handlers[lazy_type]
            else:
                self.register_type(cls, handler)
                del self._lazy_handlers[lazy_type]


describe: DescribeRegistry = DescribeRegistry()
