import abc
from collections import Counter

import attrs
from rich.text import Text

from liblaf.pretty._compile import Lowered


@attrs.define
class LowerContext:
    obj_id_counter: Counter[int]
    typenames: dict[type, str]

    def make_ref_text(self, cls: type, obj_id: int) -> Text:
        return Text.assemble(
            ("<", "repr.tag_start"),
            ("*", "repr.ellipsis"),
            # self.typenames[cls] may be empty for builtin types
            (self.typenames[cls] or cls.__name__, "repr.tag_name"),
            (" object at ", "repr.tag_contents"),
            (hex(obj_id), "repr.number"),
            (">", "repr.tag_end"),
        )


@attrs.define
class Traced(abc.ABC):
    @abc.abstractmethod
    def lower(self, ctx: LowerContext) -> Lowered: ...
