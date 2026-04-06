import attrs

from ._item import SpecItem
from ._spec import Spec


@attrs.define
class SpecItemValue(SpecItem):
    value: Spec
