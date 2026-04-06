import attrs
from rich.text import Text

from ._object import SpecObject


@attrs.define
class SpecLeaf(SpecObject):
    value: Text
