from collections.abc import Generator, Iterable
from typing import Any, cast

import attrs
from typing_extensions import Sentinel

from liblaf.pretty._conf import PrettyOptions, config
from liblaf.pretty._const import COMMA, SPACE
from liblaf.pretty._spec import SpecItem, SpecNode, TraceContext

from ._registry import DescribeRegistry, describe

TRUNCATED = Sentinel("TRUNCATED")


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
