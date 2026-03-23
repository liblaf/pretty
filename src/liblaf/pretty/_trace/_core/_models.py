from __future__ import annotations

import attrs
from rich.text import Text


@attrs.define
class TracedLiteral:
    value: Text = attrs.field(converter=lambda value: value.copy())


@attrs.define
class TracedNode:
    obj_id: int
    cls: type
    referable: bool
    appearance_count: int = attrs.field(default=1, kw_only=True)


@attrs.define
class TracedLeafNode(TracedNode):
    value: Text = attrs.field(converter=lambda value: value.copy())


@attrs.define
class TracedOccurrence:
    node: TracedNode
    kind: str
    path: tuple[int, ...]
    depth: int
    ancestors: tuple[int, ...] = attrs.field(factory=tuple, repr=False)


type TracedChild = TracedLiteral | TracedOccurrence


@attrs.define
class TracedItem:
    prefix_break: bool = attrs.field(default=False, kw_only=True)
    trailing_comma: bool = attrs.field(default=False, kw_only=True)


@attrs.define
class TracedValueItem(TracedItem):
    child: TracedChild = attrs.field()


@attrs.define
class TracedEntryItem(TracedItem):
    key: TracedChild = attrs.field()
    value: TracedChild = attrs.field()


@attrs.define
class TracedFieldItem(TracedItem):
    name: str = attrs.field()
    value: TracedChild = attrs.field()


@attrs.define
class TracedContainerNode(TracedNode):
    open_brace: str
    close_brace: str
    empty_open_brace: str
    empty_close_brace: str
    show_type_name: bool = attrs.field(default=False)
    trailing_comma_single: bool = attrs.field(default=False)
    source_items: tuple[object, ...] = attrs.field(factory=tuple, repr=False)
    items: tuple[TracedItem, ...] = attrs.field(factory=tuple)
    expanded: bool = attrs.field(default=False)


@attrs.define
class TraceResult:
    root: TracedOccurrence
    nodes_by_id: dict[int, TracedNode]
    tracked_types: set[type]
