from typing import ClassVar, TypedDict

import attrs
from rich.text import Text

from liblaf import conf
from liblaf.pretty.literals import INDENT


class PrettyOverrides(TypedDict, total=False):
    max_level: int
    max_list: int
    max_array: int
    max_dict: int
    max_string: int
    max_long: int
    max_other: int
    indent: Text | str
    hide_defaults: bool


@attrs.frozen
class PrettyOptions:
    max_level: int
    max_list: int
    max_array: int
    max_dict: int
    max_string: int
    max_long: int
    max_other: int
    indent: Text
    hide_defaults: bool


def _as_text(value: str | Text) -> Text:
    if isinstance(value, Text):
        return value
    if "\x1b" in value:
        return Text.from_ansi(value)
    return Text.from_markup(value)


def field_text(*, default: Text) -> conf.Field[Text]:
    return conf.field(default=default, converter=_as_text)


class PrettyConfig(conf.BaseConfig):
    env_prefix: ClassVar[str] = "PRETTY_"

    max_level: conf.Field[int] = conf.field_int(default=6)
    max_list: conf.Field[int] = conf.field_int(default=6)
    max_array: conf.Field[int] = conf.field_int(default=5)
    max_dict: conf.Field[int] = conf.field_int(default=4)
    max_string: conf.Field[int] = conf.field_int(default=30)
    max_long: conf.Field[int] = conf.field_int(default=40)
    max_other: conf.Field[int] = conf.field_int(default=30)
    indent: conf.Field[Text] = field_text(default=INDENT)
    hide_defaults: conf.Field[bool] = conf.field_bool(default=True)

    def dump(self) -> PrettyOptions:
        return PrettyOptions(**self.to_dict())


config: PrettyConfig = PrettyConfig()
