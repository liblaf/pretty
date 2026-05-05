from __future__ import annotations

from collections.abc import Callable
from typing import Any

import attrs
import pytest

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


def test_reprlib_limits_apply_to_fallback_scalars(render_plain: RenderText) -> None:
    assert render_plain(12345678901234567890, max_long=12) == "1234...67890"
    assert (
        render_plain("abcdefghijklmnopqrstuvwxyz0123456789", max_string=20)
        == "'abcdefg...23456789'"
    )


def test_numpy_arrays_render_as_shape_and_dtype_summaries(
    render_plain: RenderText,
) -> None:
    np = pytest.importorskip("numpy")

    assert render_plain(np.zeros((2, 3), dtype=np.float32)) == "f32[2,3](numpy)"
    assert render_plain(np.array([1, 2, 3], dtype=np.int64)) == "i64[3](numpy)"


def test_array_summaries_fall_back_when_dimensions_exceed_max_array(
    render_plain: RenderText,
) -> None:
    np = pytest.importorskip("numpy")

    assert render_plain(np.arange(6), max_array=5) == "array([0, 1, 2, 3, 4, 5])"


def test_torch_tensors_render_as_shape_and_dtype_summaries(
    render_plain: RenderText,
) -> None:
    torch = pytest.importorskip("torch")

    assert render_plain(torch.zeros((2, 3), dtype=torch.float32)) == (
        "torch.f32[2,3](torch)"
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


def test_rich_repr_hides_items_equal_to_their_default(
    render_plain: RenderText,
) -> None:
    class RichDefaults:
        def __rich_repr__(self) -> Any:
            yield "hidden", 1, 1
            yield "shown", 2, 1

    assert render_plain(RichDefaults()) == "RichDefaults(shown=2)"
    assert render_plain(RichDefaults(), hide_defaults=False) == (
        "RichDefaults(hidden=1, shown=2)"
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
