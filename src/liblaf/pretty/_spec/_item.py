import attrs
from rich.text import Text

from liblaf.pretty._const import EMPTY

from ._spec import Spec


@attrs.define
class SpecItem(Spec):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)
