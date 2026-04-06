import attrs
from rich.text import Text

from liblaf.pretty._const import EMPTY
from liblaf.pretty._trace import TracedItem

from ._spec import Spec


@attrs.define
class SpecItem[T: TracedItem](Spec[T]):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)
