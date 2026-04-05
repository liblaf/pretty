from __future__ import annotations

from collections import Counter

import attrs
from rich.text import Text


@attrs.define(slots=True)
class TracedDocument:
    root: Traced
    obj_id_counts: Counter[int]
    typenames: dict[type, str]


@attrs.define(slots=True)
class Traced:
    cls: type
    obj_id: int | None = None


@attrs.define(slots=True, kw_only=True)
class TracedLeaf(Traced):
    text: Text = attrs.field(converter=lambda value: value.copy())


@attrs.define(slots=True, kw_only=True)
class TracedReference(Traced):
    obj_id: int


@attrs.define(slots=True)
class TracedItem:
    pass


@attrs.define(slots=True)
class TracedValue(TracedItem):
    value: Traced | None = None


@attrs.define(slots=True)
class TracedField(TracedItem):
    name: str
    value: Traced | None = None


@attrs.define(slots=True)
class TracedKeyValue(TracedItem):
    key: Traced | None = None
    value: Traced | None = None


@attrs.define(slots=True, kw_only=True)
class TracedContainer(Traced):
    begin: Text = attrs.field(converter=lambda value: value.copy())
    end: Text = attrs.field(converter=lambda value: value.copy())
    empty: Text = attrs.field(converter=lambda value: value.copy())
    items: list[TracedItem] = attrs.field(factory=list)
    force_comma_if_single: bool = False
