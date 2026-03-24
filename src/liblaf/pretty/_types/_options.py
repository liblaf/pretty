import dataclasses
from typing import Any, Self

from rich.text import Text

from liblaf.pretty._compile import INDENT


@dataclasses.dataclass(frozen=True, slots=True)
class PrettyOptions:
    hide_defaults: bool = True
    indent: Text = dataclasses.field(default_factory=INDENT.copy)
    max_array: int = 5
    max_dict: int = 4
    max_level: int = 6
    max_list: int = 6
    max_long: int = 40
    max_other: int = 30
    max_string: int = 30
    max_width: int = 88

    def replace(self, **changes: Any) -> Self:
        return dataclasses.replace(self, **changes)
