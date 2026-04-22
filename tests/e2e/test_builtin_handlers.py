from __future__ import annotations

from collections.abc import Callable
from typing import Any

import attrs

type RenderText = Callable[..., str]


def test_builtin_scalar_and_container_handlers_render_python_like_output(
    render_plain: RenderText,
) -> None:
    true_value = True
    false_value = False

    assert render_plain(set()) == "set()"
    assert render_plain(frozenset()) == "frozenset()"
    assert render_plain((1,)) == "(1,)"
    assert render_plain(None) == "None"
    assert render_plain(true_value) == "True"
    assert render_plain(false_value) == "False"
    assert render_plain(...) == "..."
    assert render_plain("abcdefghijklmnopqrstuvwxyz0123456789") == (
        "'abcdefghijkl...xyz0123456789'"
    )


def test_orderable_sets_and_frozensets_render_in_sorted_order(
    render_plain: RenderText,
) -> None:
    assert render_plain({3, 1, 2}) == "{1, 2, 3}"
    assert render_plain(frozenset({3, 1, 2})) == "frozenset({1, 2, 3})"


def test_unsortable_mapping_items_keep_their_original_order(
    render_plain: RenderText,
) -> None:
    class Key:
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self) -> str:
            return self.name

    obj = {Key("b"): 2, Key("a"): 1}

    assert render_plain(obj) == "{b: 2, a: 1}"


def test_fieldz_models_hide_defaults_and_skip_repr_false_fields(
    render_plain: RenderText,
) -> None:
    @attrs.define
    class FieldzThing:
        x: int = 1
        y: int = 2
        z: int = attrs.field(default=3, repr=False)

    assert render_plain(FieldzThing()) == "FieldzThing()"
    assert render_plain(FieldzThing(y=9)) == "FieldzThing(y=9)"
    assert render_plain(FieldzThing(), hide_defaults=False) == "FieldzThing(x=1, y=2)"


def test_rich_repr_supports_pairs_falsey_names_and_positional_items(
    render_plain: RenderText,
) -> None:
    class RichVariants:
        def __rich_repr__(self) -> Any:
            yield "", 1
            yield None, 2
            yield "named", 3
            yield ("tail",)
            yield "value"

    assert (
        render_plain(RichVariants()) == "RichVariants(1, 2, named=3, 'tail', 'value')"
    )


def test_rich_repr_returning_none_falls_back_to_repr(render_plain: RenderText) -> None:
    class RichDecline:
        def __repr__(self) -> str:
            return "RichDecline<fallback>"

        def __rich_repr__(self) -> Any:
            return None

    assert render_plain(RichDecline()) == "RichDecline<fallback>"


def test_rich_repr_handles_uncomparable_defaults_without_crashing(
    render_plain: RenderText,
) -> None:
    class BoomEq:
        __hash__ = object.__hash__

        def __eq__(self, other: object) -> bool:
            del other
            msg = "boom"
            raise RuntimeError(msg)

        def __repr__(self) -> str:
            return "BoomEq()"

    class RichUncomparableDefault:
        def __rich_repr__(self) -> Any:
            yield "boom", BoomEq(), BoomEq()

    assert render_plain(RichUncomparableDefault()) == (
        "RichUncomparableDefault(boom=BoomEq())"
    )
