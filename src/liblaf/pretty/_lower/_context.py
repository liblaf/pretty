import attrs
from rich.text import Text

from .._compile import INDENT


@attrs.define(frozen=True)
class ReferenceFormatter:
    def inline_ref(self, cls: type, obj_id: int, typenames: dict[type, str]) -> Text:
        return Text.assemble(
            ("<", "repr.tag_start"),
            ("*", "repr.ellipsis"),
            (typenames[cls] or cls.__name__, "repr.tag_name"),
            (" object at ", "repr.tag_contents"),
            (hex(obj_id), "repr.number"),
            (">", "repr.tag_end"),
        )

    def anchor_annotation(
        self, cls: type, obj_id: int, typenames: dict[type, str]
    ) -> Text:
        return Text.assemble(
            "  # ", self.inline_ref(cls, obj_id, typenames).plain, style="dim"
        )


@attrs.define(frozen=True)
class LowerContext:
    typenames: dict[type, str]
    indent: Text = attrs.field(factory=lambda: INDENT.copy())
    reference_formatter: ReferenceFormatter = attrs.field(factory=ReferenceFormatter)
