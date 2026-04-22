from __future__ import annotations

from typing import Any

import attrs
from rich.console import Console

from liblaf.pretty import pformat


def render_to_plain(obj: object, /, *, width: int = 80, **kwargs: object) -> str:
    console = Console(width=width, color_system=None, soft_wrap=True)
    return pformat(obj, **kwargs).to_plain(console)


def test_builtin_scalar_and_container_handlers_render_python_like_output() -> None:
    true_value = True
    false_value = False

    assert render_to_plain(set()) == "set()"
    assert render_to_plain(frozenset()) == "frozenset()"
    assert render_to_plain((1,)) == "(1,)"
    assert render_to_plain(None) == "None"
    assert render_to_plain(true_value) == "True"
    assert render_to_plain(false_value) == "False"
    assert render_to_plain(...) == "..."
    assert render_to_plain("abcdefghijklmnopqrstuvwxyz0123456789") == (
        "'abcdefghijkl...xyz0123456789'"
    )


def test_unsortable_mapping_items_keep_their_original_order() -> None:
    class Key:
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self) -> str:
            return self.name

    obj = {Key("b"): 2, Key("a"): 1}

    assert render_to_plain(obj) == "{b: 2, a: 1}"


def test_fieldz_models_hide_defaults_and_skip_repr_false_fields() -> None:
    @attrs.define
    class FieldzThing:
        x: int = 1
        y: int = 2
        z: int = attrs.field(default=3, repr=False)

    assert render_to_plain(FieldzThing()) == "FieldzThing()"
    assert render_to_plain(FieldzThing(y=9)) == "FieldzThing(y=9)"
    assert (
        render_to_plain(FieldzThing(), hide_defaults=False) == "FieldzThing(x=1, y=2)"
    )


def test_rich_repr_supports_default_filtering_and_positional_items() -> None:
    class RichDefaults:
        def __rich_repr__(self) -> Any:
            yield "visible", 2, 1
            yield "hidden", 1, 1
            yield ("tail",)
            yield "value"

    assert render_to_plain(RichDefaults()) == "RichDefaults(visible=2, 'tail', 'value')"
    assert render_to_plain(RichDefaults(), hide_defaults=False) == (
        "RichDefaults(visible=2, hidden=1, 'tail', 'value')"
    )


def test_rich_repr_handles_uncomparable_defaults_without_crashing() -> None:
    class BoomEq:
        __hash__ = object.__hash__

        def __eq__(self, other: object) -> bool:
            msg = "boom"
            raise RuntimeError(msg)

        def __repr__(self) -> str:
            return "BoomEq()"

    class RichUncomparableDefault:
        def __rich_repr__(self) -> Any:
            yield "boom", BoomEq(), BoomEq()

    assert render_to_plain(RichUncomparableDefault()) == (
        "RichUncomparableDefault(boom=BoomEq())"
    )
