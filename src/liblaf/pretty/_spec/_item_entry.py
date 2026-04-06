import attrs
from rich.text import Text

from liblaf.pretty._const import COMMA

from ._item import SpecItem
from ._spec import Spec


@attrs.define
class SpecItemEntry(SpecItem):
    key: Spec
    value: Spec
    sep: Text = COMMA
