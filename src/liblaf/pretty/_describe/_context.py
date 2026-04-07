"""Helpers for building spec nodes during the describe stage."""

from collections.abc import Generator, Iterable
from typing import Any, cast

import attrs
from rich.text import Text

from liblaf.pretty._conf import PrettyOptions, config
from liblaf.pretty._const import COLON, COMMA, EQUAL, SPACE
from liblaf.pretty._spec import (
    SpecDictItem,
    SpecItem,
    SpecNamedItem,
    SpecNode,
    SpecValueItem,
    TraceContext,
)
from liblaf.pretty._trace import TRUNCATED, Ref
from liblaf.pretty._utils import as_text

from ._registry import DescribeRegistry, describe


@attrs.define
class DescribeContext:
    """Build spec nodes for custom pretty integrations.

    The context carries the active formatting options and the registry used to
    describe nested values. Custom ``__pretty__(ctx, depth)`` hooks can use its
    helpers to build consistent separators, truncation markers, and references.
    """

    options: PrettyOptions = attrs.field(factory=config.dump)
    registry: DescribeRegistry = attrs.field(default=describe, repr=False)

    def add_separators(self, items: Iterable[SpecItem]) -> list[SpecItem]:
        """Attach standard spacing and trailing commas to items."""
        items: list[SpecItem] = list(items)
        for i, item in enumerate(items):
            if i > 0:
                item.prefix = SPACE
            if i < len(items) - 1:
                item.suffix = COMMA
        return items

    def describe(self, obj: Any) -> SpecNode:
        """Describe an object with the active registry."""
        return self.registry.describe_lazy(obj, self)

    def describe_dict_item(
        self, key: Any, value: Any, *, sep: Text = COLON
    ) -> SpecItem:
        """Build a dictionary-style item from a key and value."""
        if key is TRUNCATED or value is TRUNCATED:
            return SpecValueItem.ellipsis()
        key_spec: SpecNode = self.describe(key)
        value_spec: SpecNode = self.describe(value)
        return SpecDictItem(key_spec, value_spec, sep=sep)

    def describe_named_item(
        self, name: str | Text, value: Any, *, sep: Text = EQUAL
    ) -> SpecItem:
        """Build a ``name=value`` item."""
        if value is TRUNCATED:
            return SpecValueItem.ellipsis()
        name: Text = as_text(name)
        spec: SpecNode = self.describe(value)
        return SpecNamedItem(name, spec, sep=sep)

    def describe_value_item(self, obj: Any) -> SpecValueItem:
        """Build a positional value item."""
        if obj is TRUNCATED:
            return SpecValueItem.ellipsis()
        spec: SpecNode = self.describe(obj)
        return SpecValueItem(spec)

    def ellipsis(self) -> SpecValueItem:
        """Build an ellipsis item."""
        return SpecValueItem.ellipsis()

    def ref(self, obj: Any) -> Ref:
        """Create a reference token for an object."""
        return Ref.from_obj(obj)

    def truncate_dict[T](self, items: Iterable[T]) -> Generator[T]:
        """Yield dictionary entries up to ``max_dict`` and then an ellipsis."""
        for i, item in enumerate(items):
            if i >= self.options.max_dict:
                yield cast("T", (TRUNCATED, TRUNCATED))
                break
            yield item

    def truncate_list[T](self, iterable: Iterable[T]) -> Generator[T]:
        """Yield list items up to ``max_list`` and then an ellipsis."""
        for i, item in enumerate(iterable):
            if i >= self.options.max_list:
                yield cast("T", TRUNCATED)
                break
            yield item

    def finish(self) -> TraceContext:
        """Create the trace-stage context for the next pipeline step."""
        ctx: TraceContext = TraceContext(options=self.options)
        return ctx
