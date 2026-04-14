"""Registration helpers for custom pretty handlers."""

from __future__ import annotations

import functools
import logging
import sys
import types
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, NamedTuple, Protocol, overload

import attrs

from liblaf.pretty.stages.wrapped import WrappedNode

from ._repr import pretty_repr

if TYPE_CHECKING:
    from ._context import PrettyContext


logger: logging.Logger = logging.getLogger(__name__)


class PrettyHandler[T](Protocol):
    """Callable that turns an object into a wrapped node or returns `None`."""

    def __call__(self, obj: T, ctx: PrettyContext, /) -> WrappedNode | None: ...


class _LazyType(NamedTuple):
    module: str
    name: str


def _default_type_dispatcher() -> functools._SingleDispatchCallable[WrappedNode | None]:
    @functools.singledispatch
    def type_dispatcher(obj: Any, ctx: PrettyContext) -> WrappedNode | None:
        del obj, ctx
        return None

    return type_dispatcher


@attrs.define
class PrettyRegistry:
    """Dispatch custom handlers before falling back to repr-style formatting."""

    handlers: list[PrettyHandler[Any]] = attrs.field(factory=list)
    lazy_handlers: dict[_LazyType, PrettyHandler[Any]] = attrs.field(factory=dict)
    type_dispatcher: functools._SingleDispatchCallable[WrappedNode | None] = (
        attrs.field(factory=_default_type_dispatcher)
    )

    def __call__(self, obj: Any, ctx: PrettyContext) -> WrappedNode:
        """Resolve one object to a wrapped node."""
        if (pretty := getattr(obj, "__pretty__", None)) is not None and (
            wrapped := pretty(ctx)
        ) is not None:
            return wrapped
        self.resolve_lazy()
        if (wrapped := self.type_dispatcher(obj, ctx)) is not None:
            return wrapped
        for handler in reversed(self.handlers):
            if (wrapped := handler(obj, ctx)) is not None:
                return wrapped
        return pretty_repr(obj, ctx)

    def register_func[F: PrettyHandler[Any]](self, func: F) -> F:
        """Register a structural handler.

        Structural handlers run after type-based dispatch and may return `None`
        to fall through to the next handler.
        """
        self.handlers.append(func)
        return func

    @overload
    def register_lazy[F: PrettyHandler[Any]](
        self, module: str, name: str, func: F
    ) -> F: ...
    @overload
    def register_lazy[F: PrettyHandler[Any]](
        self, module: str, name: str, func: None = None
    ) -> Callable[[F], F]: ...
    def register_lazy[F: PrettyHandler[Any]](
        self, module: str, name: str, func: F | None = None
    ) -> Callable[..., Any]:
        """Register a handler for a type that may be imported later."""
        if func is None:
            return functools.partial(self.register_lazy, module, name)
        self.lazy_handlers[_LazyType(module, name)] = func
        return func

    @overload
    def register_type[F: PrettyHandler[Any]](self, cls: type, func: F) -> F: ...
    @overload
    def register_type[F: PrettyHandler[Any]](
        self, cls: type, func: None = None
    ) -> Callable[[F], F]: ...
    def register_type[F: PrettyHandler[Any]](
        self, cls: type, func: F | None = None
    ) -> Callable[..., Any]:
        """Register a handler for a concrete Python class."""
        if func is None:
            return functools.partial(self.register_type, cls)
        return self.type_dispatcher.register(cls, func)

    def resolve_lazy(self) -> None:
        """Attach lazy handlers whose modules are already imported."""
        for (module_name, cls_name), handler in list(self.lazy_handlers.items()):
            module: types.ModuleType | None = sys.modules.get(module_name)
            if module is None:
                continue
            try:
                cls: type = getattr(module, cls_name)
            except AttributeError:
                logger.exception("")
            else:
                self.register_type(cls, handler)
            finally:
                del self.lazy_handlers[_LazyType(module_name, cls_name)]


registry: PrettyRegistry = PrettyRegistry()
register_func = registry.register_func
register_lazy = registry.register_lazy
register_type = registry.register_type
