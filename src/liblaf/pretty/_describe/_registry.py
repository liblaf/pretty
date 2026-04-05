from __future__ import annotations

import functools
import logging
import sys
from collections.abc import Callable
from typing import Any, Protocol, overload

import attrs

from liblaf.pretty._options import PrettyOptions
from liblaf.pretty._spec import Spec

logger = logging.getLogger(__name__)


class DescribeTypeHandler[T](Protocol):
    def __call__(self, obj: T, options: PrettyOptions, /) -> Spec | None: ...


class DescribeFunc(Protocol):
    def __call__(self, obj: object, options: PrettyOptions, /) -> Spec | None: ...


def _default_dispatcher() -> functools._SingleDispatchCallable[Spec | None]:
    @functools.singledispatch
    def dispatcher(_obj: object, _options: PrettyOptions) -> Spec | None:
        return None

    return dispatcher


@attrs.define
class DescribeRegistry:
    dispatcher: functools._SingleDispatchCallable[Spec | None] = attrs.field(
        factory=_default_dispatcher
    )
    handlers: list[DescribeFunc] = attrs.field(factory=list)
    handlers_lazy: dict[tuple[str, str], DescribeTypeHandler[Any]] = attrs.field(
        factory=dict
    )

    def __call__(self, obj: object, options: PrettyOptions) -> Spec | None:
        self._resolve_lazy()
        result: Spec | None = self.dispatcher(obj, options)
        if result is not None:
            return result
        for handler in self.handlers:
            result = handler(obj, options)
            if result is not None:
                return result
        return None

    @overload
    def register_type[F: DescribeTypeHandler[Any]](
        self, cls: type, handler: F
    ) -> F: ...

    @overload
    def register_type[F: DescribeTypeHandler[Any]](
        self, cls: type, handler: None = None
    ) -> Callable[[F], F]: ...

    def register_type(
        self, cls: type, handler: DescribeTypeHandler[Any] | None = None
    ) -> Callable[..., Any]:
        return self.dispatcher.register(cls, handler)

    @overload
    def register_lazy[F: DescribeTypeHandler[Any]](
        self, module: str, typename: str, handler: F
    ) -> F: ...

    @overload
    def register_lazy[F: DescribeTypeHandler[Any]](
        self, module: str, typename: str, handler: None = None
    ) -> Callable[[F], F]: ...

    def register_lazy(
        self,
        module: str,
        typename: str,
        handler: DescribeTypeHandler[Any] | None = None,
    ) -> Callable[..., Any]:
        if handler is None:
            return functools.partial(self.register_lazy, module, typename)
        self.handlers_lazy[(module, typename)] = handler
        return handler

    def register_func[F: DescribeFunc](self, handler: F) -> F:
        self.handlers.append(handler)
        return handler

    def _resolve_lazy(self) -> None:
        for (module_name, typename), handler in list(self.handlers_lazy.items()):
            module = sys.modules.get(module_name)
            if module is None:
                continue
            try:
                cls: type = getattr(module, typename)
            except AttributeError:
                logger.exception("")
            else:
                self.register_type(cls, handler)
                del self.handlers_lazy[(module_name, typename)]


describe_registry = DescribeRegistry()
register_func = describe_registry.register_func
register_lazy = describe_registry.register_lazy
register_type = describe_registry.register_type
