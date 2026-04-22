"""Context helpers exposed to custom pretty-printers.

`PrettyContext` is shared across the full formatting pass. Custom handlers use
it to build wrapped nodes, while later pipeline stages reuse the same context
for truncation rules, fallback repr configuration, and reference tracking.
"""

import functools
import reprlib
from collections import deque
from collections.abc import Callable, Generator, Iterable
from typing import Any

import attrs
from rich.text import Text

from liblaf.pretty.common import TRUNCATED, ObjectIdentifier
from liblaf.pretty.literals import COMMA, SPACE
from liblaf.pretty.stages.traced import TracedNode
from liblaf.pretty.stages.wrapped import (
    TraceContext,
    WrappedChild,
    WrappedContainer,
    WrappedItem,
    WrappedKeyValueItem,
    WrappedLazy,
    WrappedLeaf,
    WrappedNameValueItem,
    WrappedNode,
    WrappedPositionalItem,
)

from ._registry import PrettyRegistry, registry


@attrs.define
class PrettyContext(TraceContext):
    """Helper object passed to custom formatters and pipeline stages.

    Custom handlers usually build output with [`container`][liblaf.pretty.custom.PrettyContext.container],
    [`name_value`][liblaf.pretty.custom.PrettyContext.name_value], and
    [`positional`][liblaf.pretty.custom.PrettyContext.positional].

    Attributes:
        registry: Handler registry consulted when wrapping objects.
        wrap_cache: Per-pass cache keyed by `id(obj)` so repeated references
            keep their identity through the pipeline.
    """

    registry: PrettyRegistry = attrs.field(default=registry)
    wrap_cache: dict[int, WrappedNode] = attrs.field(factory=dict)

    @functools.cached_property
    def arepr(self) -> reprlib.Repr:
        """Return the configured `reprlib.Repr` instance used for fallback formatting.

        The limits mirror the active [`PrettyOptions`][liblaf.pretty.PrettyOptions].
        """
        arepr: reprlib.Repr = reprlib.Repr(
            maxlevel=self.options.max_level,
            maxtuple=self.options.max_list,
            maxlist=self.options.max_list,
            maxarray=self.options.max_array,
            maxdict=self.options.max_dict,
            maxfrozenset=self.options.max_list,
            maxdeque=self.options.max_list,
            maxstring=self.options.max_string,
            maxlong=self.options.max_long,
            maxother=self.options.max_other,
            indent=self.options.indent.plain,
        )
        return arepr

    def ellipsis_item(self) -> WrappedItem:
        """Return the positional ellipsis item used for truncated containers."""
        return WrappedPositionalItem.ellipsis()

    def identifier(self, obj: Any) -> ObjectIdentifier:
        """Return the identity record for `obj`."""
        return ObjectIdentifier.from_obj(obj)

    def trace(self, root: WrappedNode) -> TracedNode:
        """Trace wrapped nodes and attach reference information."""
        children, traced_root = root.trace(self)
        queue: deque[WrappedChild] = deque(children)
        while queue:
            wrapped, self.depth, attach = queue.popleft()
            children, traced = wrapped.trace(self)
            queue.extend(children)
            attach(traced)
        return traced_root

    def wrap_eager(self, obj: Any) -> WrappedNode:
        """Wrap `obj` immediately and memoize the result by object identity.

        This preserves shared references for referencable objects and avoids
        rebuilding the same wrapped node repeatedly during one pass.
        """
        id_: int = id(obj)
        if (wrapped := self.wrap_cache.get(id_)) is not None:
            return wrapped
        wrapped: WrappedNode = self.registry(obj, self)
        self.wrap_cache[id_] = wrapped
        return wrapped

    def wrap_lazy(self, obj: Any) -> WrappedLazy:
        """Create a lazily wrapped placeholder for `obj`.

        Lazy children delay the actual wrapping work until the trace step asks
        for them.
        """
        return WrappedLazy(
            factory=lambda: self.wrap_eager(obj), identifier=self.identifier(obj)
        )

    # ------------------------------ truncate_* ------------------------------ #

    def truncate_dict[K, V](
        self, items: Iterable[tuple[K, V]]
    ) -> Generator[tuple[K, V]]:
        """Yield mapping items up to `max_dict`, then a truncation marker."""
        for i, item in enumerate(items):
            if i >= self.options.max_dict:
                yield TRUNCATED, TRUNCATED
                break
            yield item

    def truncate_list[T](self, items: Iterable[T]) -> Generator[T]:
        """Yield list-like items up to `max_list`, then a truncation marker."""
        for i, item in enumerate(items):
            if i >= self.options.max_list:
                yield TRUNCATED
                break
            yield item

    # ------------------------------ WrappedItem ----------------------------- #

    def key_value(self, key: Any, value: Any) -> WrappedItem:
        """Build a `key: value` item or an ellipsis placeholder when truncated."""
        if key is TRUNCATED or value is TRUNCATED:
            return self.ellipsis_item()
        return WrappedKeyValueItem(key=self.wrap_lazy(key), value=self.wrap_lazy(value))

    def name_value(self, name: str | Text | None, value: Any) -> WrappedItem:
        """Build a repr-style `name=value` item.

        Falsey names fall back to [`positional`][liblaf.pretty.custom.PrettyContext.positional].
        """
        if not name:
            return self.positional(value)
        if isinstance(name, str):
            name = Text(name, "repr.attrib_name")
        return WrappedNameValueItem(name=name, value=self.wrap_lazy(value))

    def positional(self, value: Any) -> WrappedItem:
        """Build a positional item or an ellipsis placeholder when truncated."""
        if value is TRUNCATED:
            return self.ellipsis_item()
        return WrappedPositionalItem(value=self.wrap_lazy(value))

    # ------------------------------ WrappedNode ----------------------------- #

    def container(
        self,
        obj: Any,
        begin: Text,
        children: Iterable[WrappedItem],
        end: Text,
        indent: Text | None = None,
        *,
        add_separators: bool = True,
        empty: Text | None = None,
        referencable: bool = True,
    ) -> WrappedContainer:
        """Build a repr-like container node.

        Args:
            obj: Original object represented by the container.
            begin: Opening punctuation, usually styled Rich text such as `(` or `[`.
            children: Wrapped child items to render inside the container.
            end: Closing punctuation.
            indent: Indentation used for wrapped layouts. Defaults to the active
                formatter option.
            add_separators: When `True`, add repr-style spaces and commas between
                children before building the container.
            empty: Alternate rendering for empty containers such as `set()`.
            referencable: Whether repeated appearances of `obj` should be rendered as
                shared references later in the pipeline.

        Returns:
            A wrapped container ready for tracing and lowering.

        Note:
            Containers are referencable by default. Repeated appearances of the
            same container can therefore render as shared-reference tags later
            in the pipeline.
        """
        if indent is None:
            indent: Text = self.options.indent
        if add_separators:
            children: list[WrappedItem] = self.add_separators(children)
        kwargs: dict[str, Any] = {}
        if empty is not None:
            kwargs["empty"] = empty
        return WrappedContainer(
            begin=begin,
            children=children,
            end=end,
            indent=indent,
            identifier=self.identifier(obj),
            referencable=referencable,
            **kwargs,
        )

    def leaf(self, obj: Any, text: Text, *, referencable: bool = True) -> WrappedLeaf:
        """Build a scalar leaf node from Rich text.

        Set `referencable=False` for scalar summaries that should always render
        inline instead of turning into shared-reference tags.
        """
        return WrappedLeaf(
            value=text, identifier=self.identifier(obj), referencable=referencable
        )

    # --------------------------------- utils -------------------------------- #

    @staticmethod
    def add_separators(items: Iterable[WrappedItem]) -> list[WrappedItem]:
        """Add repr-style spacing and trailing commas to a sequence of items."""
        items: list[WrappedItem] = list(items)
        for i, item in enumerate(items):
            if i > 0:
                item.prefix = SPACE
            if i < len(items) - 1:
                item.suffix = COMMA
        return items

    @staticmethod
    def possibly_sorted[T](
        items: Iterable[T],
        *,
        key: Callable[[T], Any] | None = None,
        reverse: bool = False,
    ) -> Iterable[T]:
        """Sort items when possible, otherwise preserve their original order.

        This keeps set- and dict-like output stable when the items are
        orderable, while still handling unorderable objects gracefully.
        """
        try:
            return sorted(items, key=key, reverse=reverse)
        except Exception:  # noqa: BLE001
            return items
