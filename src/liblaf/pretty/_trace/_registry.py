from __future__ import annotations

import functools
import logging
import sys
import types
from collections.abc import Callable
from importlib import import_module
from typing import Any, Protocol, overload

import attrs

from liblaf.pretty._trace._helpers._builder import PrettyBuilder
from liblaf.pretty._trace._helpers._specs import PrettySpec

logger: logging.Logger = logging.getLogger(__name__)


class PrettyAdapter[T](Protocol):
    def __call__(self, obj: T, builder: PrettyBuilder, /) -> PrettySpec | None: ...


def _default_dispatcher() -> functools._SingleDispatchCallable[PrettySpec | None]:
    @functools.singledispatch
    def dispatcher(_obj: Any, _builder: PrettyBuilder) -> PrettySpec | None:
        return None

    return dispatcher


@attrs.define
class PrettyRegistry:
    dispatcher: functools._SingleDispatchCallable[PrettySpec | None] = attrs.field(
        factory=_default_dispatcher
    )
    fallbacks: list[PrettyAdapter[Any]] = attrs.field(factory=list)
    handlers_lazy: dict[tuple[str, str], PrettyAdapter[Any]] = attrs.field(factory=dict)

    @functools.cached_property
    def _default_handler(self) -> PrettyAdapter[Any]:
        return self.dispatcher.dispatch(object)

    def resolve(self, obj: Any) -> PrettyAdapter[Any] | None:
        self._resolve_lazy()
        handler: PrettyAdapter[Any] = self.dispatcher.dispatch(type(obj))
        if handler is not self._default_handler:
            return handler
        if self.fallbacks:
            return self._run_fallbacks
        return None

    @overload
    def register[F: PrettyAdapter[Any]](self, cls: type, handler: F) -> F: ...
    @overload
    def register[F: PrettyAdapter[Any]](
        self, cls: type, handler: None = None
    ) -> Callable[[F], F]: ...
    def register(
        self, cls: type, handler: PrettyAdapter[Any] | None = None
    ) -> Callable[..., Any]:
        return self.dispatcher.register(cls, handler)

    def register_fallback[F: PrettyAdapter[Any]](self, handler: F) -> F:
        self.fallbacks.append(handler)
        return handler

    @overload
    def register_lazy[F: PrettyAdapter[Any]](
        self, module: str, typename: str, handler: F
    ) -> F: ...
    @overload
    def register_lazy[F: PrettyAdapter[Any]](
        self, module: str, typename: str, handler: None = None
    ) -> Callable[[F], F]: ...
    def register_lazy(
        self, module: str, typename: str, handler: PrettyAdapter[Any] | None = None
    ) -> Callable[..., Any]:
        if handler is None:
            return functools.partial(self.register_lazy, module, typename)
        self.handlers_lazy[(module, typename)] = handler
        return handler

    def _run_fallbacks(self, obj: Any, builder: PrettyBuilder) -> PrettySpec | None:
        for handler in reversed(self.fallbacks):
            result: PrettySpec | None = handler(obj, builder)
            if result is not None:
                return result
        return None

    def _resolve_lazy(self) -> None:
        for name in ("_array", "_containers", "_fieldz", "_rich_repr", "_scalars"):
            import_module(f"liblaf.pretty._prelude._builtin.{name}")

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


registry: PrettyRegistry = PrettyRegistry()
