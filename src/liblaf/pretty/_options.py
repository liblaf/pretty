from __future__ import annotations

import attrs
from rich.text import Text


def _to_text(value: Text | str) -> Text:
    if isinstance(value, Text):
        return value.copy()
    return Text(str(value))


def _default_indent() -> Text:
    return Text("\N{BOX DRAWINGS LIGHT VERTICAL}   ", "repr.indent")


def _validate_positive(
    _instance: object, attribute: attrs.Attribute[int], value: int
) -> None:
    if value <= 0:
        msg = f"{attribute.name} must be positive"
        raise ValueError(msg)


@attrs.frozen(hash=False)
class PrettyOptions:
    indent: Text = attrs.field(factory=_default_indent, converter=_to_text)
    max_dict: int = attrs.field(default=4, validator=_validate_positive)
    max_level: int = attrs.field(default=6, validator=_validate_positive)
    max_list: int = attrs.field(default=6, validator=_validate_positive)
    max_long: int = attrs.field(default=40, validator=_validate_positive)
    max_other: int = attrs.field(default=30, validator=_validate_positive)
    max_string: int = attrs.field(default=30, validator=_validate_positive)
    max_width: int = attrs.field(default=88, validator=_validate_positive)
