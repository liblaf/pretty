import contextlib
import contextvars
from collections.abc import Generator
from typing import Self, TypedDict, Unpack

import attrs
from rich.text import Text

from liblaf.pretty._compile import INDENT

from ._fields import BoolField, ConfigField, IntField, TextField


class PrettyOptions(TypedDict, total=False):
    hide_defaults: bool
    indent: Text
    max_array: int
    max_dict: int
    max_level: int
    max_list: int
    max_long: int
    max_other: int
    max_string: int
    max_width: int


@attrs.define
class PrettyConfigState:
    hide_defaults: bool
    indent: Text
    max_array: int
    max_dict: int
    max_level: int
    max_list: int
    max_long: int
    max_other: int
    max_string: int
    max_width: int


class PrettyConfig:
    hide_defaults: BoolField = BoolField("hide_defaults", True)  # noqa: FBT003
    indent: TextField = TextField("indent", INDENT)
    max_array: IntField = IntField("max_array", 5)
    max_dict: IntField = IntField("max_dict", 4)
    max_level: IntField = IntField("max_level", 6)
    max_list: IntField = IntField("max_list", 6)
    max_long: IntField = IntField("max_long", 40)
    max_other: IntField = IntField("max_other", 30)
    max_string: IntField = IntField("max_string", 30)
    max_width: IntField = IntField("max_width", 88)

    def dump(self) -> PrettyConfigState:
        return PrettyConfigState(
            hide_defaults=self.hide_defaults.get(),
            indent=self.indent.get(),
            max_array=self.max_array.get(),
            max_dict=self.max_dict.get(),
            max_level=self.max_level.get(),
            max_list=self.max_list.get(),
            max_long=self.max_long.get(),
            max_other=self.max_other.get(),
            max_string=self.max_string.get(),
            max_width=self.max_width.get(),
        )

    @contextlib.contextmanager
    def override(self, **kwargs: Unpack[PrettyOptions]) -> Generator[Self]:
        tokens: dict[ConfigField, contextvars.Token] = {}
        for name, value in kwargs.items():
            field: ConfigField = getattr(self, name)
            tokens[field] = field.var.set(value)
        try:
            yield self
        finally:
            for field, token in tokens.items():
                field.var.reset(token)


config = PrettyConfig()
