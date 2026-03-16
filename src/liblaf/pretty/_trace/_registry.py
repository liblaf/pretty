from __future__ import annotations

import functools
import logging
import sys
import types
from collections.abc import Callable
from typing import Any, Protocol, overload

import attrs

from liblaf.pretty._lower import Traced

from ._base import TraceContext

logger: logging.Logger = logging.getLogger(__name__)


class TraceHandler[T](Protocol):
    def __call__(self, obj: T, ctx: TraceContext, /) -> Traced | None: ...


def _default_dispatcher() -> functools._SingleDispatchCallable[Traced | None]:
    @functools.singledispatch
    def dispatcher(_obj: Any, _ctx: TraceContext) -> Traced | None:
        return None

    return dispatcher


@attrs.define
class TraceRegistry:
    dispatcher: functools._SingleDispatchCallable[Traced | None] = attrs.field(
        factory=_default_dispatcher
    )
    handlers: list[TraceHandler[Any]] = attrs.field(factory=list)
    handlers_lazy: dict[tuple[str, str], TraceHandler[Any]] = attrs.field(factory=dict)

    def __call__(self, obj: Any, ctx: TraceContext) -> Traced:
        from ._repr import trace_repr

        self._resolve_lazy()
        if hasattr(obj, "__liblaf_pretty__"):
            result: Traced | None = obj.__liblaf_pretty__(ctx)
            if result is not None:
                return result
        result: Traced | None = self.dispatcher(obj, ctx)
        if result is not None:
            return result
        for handler in reversed(self.handlers):
            result: Traced | None = handler(obj, ctx)
            if result is not None:
                return result
        return trace_repr(obj, ctx)

    @overload
    def register[F: TraceHandler[Any]](self, cls: type, handler: F) -> F: ...
    @overload
    def register[F: TraceHandler[Any]](
        self, cls: type, handler: None = None
    ) -> Callable[[F], F]: ...
    def register(
        self, cls: type, handler: TraceHandler[Any] | None = None
    ) -> Callable[..., Any]:
        return self.dispatcher.register(cls, handler)

    def register_func[F: TraceHandler[Any]](self, handler: F) -> F:
        self.handlers.append(handler)
        return handler

    @overload
    def register_lazy[F: TraceHandler[Any]](
        self, module: str, typename: str, handler: F
    ) -> F: ...
    @overload
    def register_lazy[F: TraceHandler[Any]](
        self, module: str, typename: str, handler: None = None
    ) -> Callable[[F], F]: ...
    def register_lazy(
        self, module: str, typename: str, handler: TraceHandler[Any] | None = None
    ) -> Callable[..., Any]:
        if handler is None:
            return functools.partial(self.register_lazy, module, typename)
        self.handlers_lazy[(module, typename)] = handler
        return handler

    def _resolve_lazy(self) -> None:
        from . import (  # noqa: F401
            _array,
            _builtin_containers,
            _builtin_scalars,
            _fieldz,
            _rich_repr,
        )

        for (module_name, typename), handler in list(self.handlers_lazy.items()):
            module: types.ModuleType | None = sys.modules.get(module_name)
            if module is None:
                continue
            try:
                cls: type = getattr(module, typename)
            except AttributeError:
                logger.exception("")
            else:
                self.register(cls, handler)
                del self.handlers_lazy[(module_name, typename)]


trace: TraceRegistry = TraceRegistry()
