import attrs
from rich.text import Text

from liblaf.pretty._const import EQUAL

from ._item import SpecItem
from ._spec import Spec


@attrs.define
class SpecItemField(SpecItem):
    name: Text
    value: Spec
    sep: Text = EQUAL
