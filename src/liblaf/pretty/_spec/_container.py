from collections.abc import Iterable
from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._const import INDENT

from ._item import SpecItem
from ._object import SpecObject


@attrs.define
class SpecContainer(SpecObject):
    begin: Text
    items: Iterable[SpecItem]
    end: Text

    def _default_empty(self) -> Text:
        return self.begin[0] + self.end[-1]

    empty: Text = attrs.field(
        default=attrs.Factory(_default_empty, takes_self=True), kw_only=True
    )
    indent: Text = attrs.field(default=INDENT, kw_only=True)
