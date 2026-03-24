import contextlib
import contextvars
from collections.abc import Generator
from typing import Any

from rich.text import Text

from liblaf.pretty._api._config_fields import (
    BoolField,
    ConfigField,
    IntField,
    TextField,
)
from liblaf.pretty._compile import INDENT
from liblaf.pretty._types._options import PrettyOptions

_HIDE_DEFAULTS_FIELD: BoolField = BoolField("hide_defaults", True)  # noqa: FBT003
_INDENT_FIELD: TextField = TextField("indent", INDENT)
_MAX_ARRAY_FIELD: IntField = IntField("max_array", 5)
_MAX_DICT_FIELD: IntField = IntField("max_dict", 4)
_MAX_LEVEL_FIELD: IntField = IntField("max_level", 6)
_MAX_LIST_FIELD: IntField = IntField("max_list", 6)
_MAX_LONG_FIELD: IntField = IntField("max_long", 40)
_MAX_OTHER_FIELD: IntField = IntField("max_other", 30)
_MAX_STRING_FIELD: IntField = IntField("max_string", 30)
_MAX_WIDTH_FIELD: IntField = IntField("max_width", 88)


def _default_indent() -> Text:
    return _INDENT_FIELD.get().copy()


class PrettyConfig:
    hide_defaults: ConfigField[bool] = _HIDE_DEFAULTS_FIELD
    indent: ConfigField[Text] = _INDENT_FIELD
    max_array: ConfigField[int] = _MAX_ARRAY_FIELD
    max_dict: ConfigField[int] = _MAX_DICT_FIELD
    max_level: ConfigField[int] = _MAX_LEVEL_FIELD
    max_list: ConfigField[int] = _MAX_LIST_FIELD
    max_long: ConfigField[int] = _MAX_LONG_FIELD
    max_other: ConfigField[int] = _MAX_OTHER_FIELD
    max_string: ConfigField[int] = _MAX_STRING_FIELD
    max_width: ConfigField[int] = _MAX_WIDTH_FIELD

    def __init__(self) -> None:
        self._options: contextvars.ContextVar[PrettyOptions | None] = (
            contextvars.ContextVar("pretty_options", default=None)
        )

    def get(self) -> PrettyOptions:
        options = self._options.get()
        if options is None:
            return PrettyOptions(
                hide_defaults=_HIDE_DEFAULTS_FIELD.get(),
                indent=_default_indent(),
                max_array=_MAX_ARRAY_FIELD.get(),
                max_dict=_MAX_DICT_FIELD.get(),
                max_level=_MAX_LEVEL_FIELD.get(),
                max_list=_MAX_LIST_FIELD.get(),
                max_long=_MAX_LONG_FIELD.get(),
                max_other=_MAX_OTHER_FIELD.get(),
                max_string=_MAX_STRING_FIELD.get(),
                max_width=_MAX_WIDTH_FIELD.get(),
            )
        return options

    def set(self, options: PrettyOptions) -> contextvars.Token[PrettyOptions | None]:
        return self._options.set(options)

    @contextlib.contextmanager
    def override(self, **kwargs: Any) -> Generator[PrettyOptions]:
        token: contextvars.Token[PrettyOptions | None] = self.set(
            self.get().replace(**kwargs)
        )
        try:
            yield self.get()
        finally:
            self._options.reset(token)


config = PrettyConfig()
