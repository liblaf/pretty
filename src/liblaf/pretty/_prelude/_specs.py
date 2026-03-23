import attrs
from rich.text import Text

from ._common import copy_text
from ._items import ItemSpec


@attrs.frozen
class PrettySpec:
    referable: bool = attrs.field(default=True, kw_only=True)


@attrs.frozen
class LiteralSpec(PrettySpec):
    value: Text = attrs.field(converter=copy_text)
    referable: bool = attrs.field(default=False, init=False)


@attrs.frozen
class LeafSpec(PrettySpec):
    value: Text = attrs.field(converter=copy_text)


@attrs.frozen
class ContainerSpec(PrettySpec):
    items: tuple[ItemSpec, ...] = attrs.field(converter=tuple)
    open_brace: str = attrs.field(kw_only=True)
    close_brace: str = attrs.field(kw_only=True)
    show_type_name: bool = attrs.field(default=False, kw_only=True)
    trailing_comma_single: bool = attrs.field(default=False, kw_only=True)

    def _default_empty_open_brace(self) -> str:
        return self.open_brace[0] if self.open_brace else ""

    empty_open_brace: str = attrs.field(
        default=attrs.Factory(_default_empty_open_brace, takes_self=True), kw_only=True
    )

    def _default_empty_close_brace(self) -> str:
        return self.close_brace[-1] if self.close_brace else ""

    empty_close_brace: str = attrs.field(
        default=attrs.Factory(_default_empty_close_brace, takes_self=True), kw_only=True
    )
