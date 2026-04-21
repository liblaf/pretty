"""Configuration types and environment-backed defaults for `liblaf.pretty`."""

from typing import ClassVar, TypedDict

import attrs
from rich.text import Text

from liblaf import conf
from liblaf.pretty.literals import INDENT


class PrettyOverrides(TypedDict, total=False):
    """Keyword overrides accepted by the public formatting functions.

    Attributes:
        max_level: Maximum nesting depth before values collapse to `...`.
        max_list: Maximum visible items for list-like containers.
        max_array: Maximum elements forwarded to repr-style array handlers.
        max_dict: Maximum visible key-value pairs for mappings.
        max_string: Maximum string repr length before truncation.
        max_long: Maximum integer repr length before truncation.
        max_other: Maximum repr length for other scalar values.
        indent: Indentation used when layouts wrap across lines.
        hide_defaults: Hide default-valued fields from `fieldz` and `__rich_repr__`
            output.
    """

    max_level: int
    max_list: int
    max_array: int
    max_dict: int
    max_string: int
    max_long: int
    max_other: int
    indent: str | Text
    hide_defaults: bool


def _as_text(value: str | Text) -> Text:
    """Normalize string-like indentation into Rich text."""
    if isinstance(value, Text):
        return value
    if "\x1b" in value:
        return Text.from_ansi(value)
    return Text.from_markup(value)


@attrs.frozen
class PrettyOptions:
    """Resolved options for a single formatting pass.

    These values are usually created from [`config`][liblaf.pretty.config] plus
    per-call [`PrettyOverrides`][liblaf.pretty.PrettyOverrides].

    Attributes:
        max_level: Maximum nesting depth before values collapse to `...`.
        max_list: Maximum visible items for list-like containers.
        max_array: Maximum elements forwarded to repr-style array handlers.
        max_dict: Maximum visible key-value pairs for mappings.
        max_string: Maximum string repr length before truncation.
        max_long: Maximum integer repr length before truncation.
        max_other: Maximum repr length for other scalar values.
        indent: Indentation used when layouts wrap across lines.
        hide_defaults: Hide default-valued fields from `fieldz` and `__rich_repr__`
            output.
    """

    max_level: int
    max_list: int
    max_array: int
    max_dict: int
    max_string: int
    max_long: int
    max_other: int
    indent: Text = attrs.field(converter=_as_text)
    hide_defaults: bool


def field_text(*, default: Text) -> conf.Field[Text]:
    """Create a config field that accepts markup, ANSI, or Rich text."""
    return conf.field(default=default, converter=_as_text)


class PrettyConfig(conf.BaseConfig):
    """Environment-backed defaults for the pretty printer.

    Values are loaded from `PRETTY_*` variables and can be overridden per call with
    [`pformat`][liblaf.pretty.pformat] or [`pprint`][liblaf.pretty.pprint].
    """

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
        """Materialize the current configuration as [`PrettyOptions`][liblaf.pretty.PrettyOptions]."""
        return PrettyOptions(**self.to_dict())


config: PrettyConfig = PrettyConfig()
