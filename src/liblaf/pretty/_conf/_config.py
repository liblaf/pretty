import types
from typing import ClassVar

import attrs
from rich.text import Text

from liblaf import conf
from liblaf.pretty._const import INDENT
from liblaf.pretty._utils import as_text


@attrs.frozen
class PrettyOptions(types.SimpleNamespace):
    max_level: int
    max_list: int
    max_array: int
    max_dict: int
    max_string: int
    max_long: int
    max_other: int
    fill_value: Text
    indent: Text
    hide_defaults: bool


def field_text(*, default: Text) -> conf.Field[Text]:
    return conf.field(default=default, converter=as_text)


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
