import attrs

from ._common import PrettyChild


@attrs.frozen
class ItemSpec:
    pass


@attrs.frozen
class ValueItemSpec(ItemSpec):
    child: PrettyChild


@attrs.frozen
class EntryItemSpec(ItemSpec):
    key: PrettyChild
    value: PrettyChild


@attrs.frozen
class FieldItemSpec(ItemSpec):
    name: str
    value: PrettyChild
