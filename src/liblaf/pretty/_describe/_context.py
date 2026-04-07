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
    options: PrettyOptions = attrs.field(factory=config.dump)
    registry: DescribeRegistry = attrs.field(default=describe, repr=False)

    def add_separators(self, items: Iterable[SpecItem]) -> list[SpecItem]:
        items: list[SpecItem] = list(items)
        for i, item in enumerate(items):
            if i > 0:
                item.prefix = SPACE
            if i < len(items) - 1:
                item.suffix = COMMA
        return items

    def describe(self, obj: Any) -> SpecNode:
        return self.registry.describe_lazy(obj, self)

    def describe_dict_item(
        self, key: Any, value: Any, *, sep: Text = COLON
    ) -> SpecItem:
        if key is TRUNCATED or value is TRUNCATED:
            return SpecValueItem.ellipsis()
        key_spec: SpecNode = self.describe(key)
        value_spec: SpecNode = self.describe(value)
        return SpecDictItem(key_spec, value_spec, sep=sep)

    def describe_named_item(
        self, name: str | Text, value: Any, *, sep: Text = EQUAL
    ) -> SpecItem:
        if value is TRUNCATED:
            return SpecValueItem.ellipsis()
        name: Text = as_text(name)
        spec: SpecNode = self.describe(value)
        return SpecNamedItem(name, spec, sep=sep)

    def describe_value_item(self, obj: Any) -> SpecValueItem:
        if obj is TRUNCATED:
            return SpecValueItem.ellipsis()
        spec: SpecNode = self.describe(obj)
        return SpecValueItem(spec)

    def ellipsis(self) -> SpecValueItem:
        return SpecValueItem.ellipsis()

    def ref(self, obj: Any) -> Ref:
        return Ref.from_obj(obj)

    def truncate_dict[T](self, items: Iterable[T]) -> Generator[T]:
        for i, item in enumerate(items):
            if i >= self.options.max_dict:
                yield cast("T", (TRUNCATED, TRUNCATED))
                break
            yield item

    def truncate_list[T](self, iterable: Iterable[T]) -> Generator[T]:
        for i, item in enumerate(iterable):
            if i >= self.options.max_list:
                yield cast("T", TRUNCATED)
                break
            yield item

    def finish(self) -> TraceContext:
        ctx: TraceContext = TraceContext(options=self.options)
        return ctx
