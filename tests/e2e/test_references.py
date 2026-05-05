from __future__ import annotations

from collections.abc import Callable

import pytest

type NormalizeRefs = Callable[[str], str]
type RenderText = Callable[..., str]


def test_shared_dict_references_are_annotated(
    render_plain: RenderText,
    normalize_refs: NormalizeRefs,
) -> None:
    child = {"x": 1}

    rendered = normalize_refs(render_plain({"left": child, "right": child}, width=120))

    assert rendered == (
        "{\n|   'left': {'x': 1},  # <dict @ <id>>\n|   'right': <dict @ <id>>\n}"
    )


def test_shared_dict_anchor_prefers_shallowest_reachable_path(
    render_plain: RenderText,
    normalize_refs: NormalizeRefs,
) -> None:
    child = {"x": 1}
    obj = {"deep": {"child": child}, "shallow": child}

    rendered = normalize_refs(render_plain(obj, width=120))

    assert rendered == (
        "{\n"
        "|   'deep': {'child': <dict @ <id>>},\n"
        "|   'shallow': {'x': 1}  # <dict @ <id>>\n"
        "}"
    )


def test_shared_frozenset_references_are_annotated(
    render_plain: RenderText,
    normalize_refs: NormalizeRefs,
) -> None:
    child = frozenset({1, 2})

    rendered = normalize_refs(render_plain({"left": child, "right": child}, width=120))

    assert rendered == (
        "{\n"
        "|   'left': frozenset({1, 2}),  # <frozenset @ <id>>\n"
        "|   'right': <frozenset @ <id>>\n"
        "}"
    )


@pytest.mark.parametrize(
    ("child", "expected"),
    [
        pytest.param([1, 2], "[1, 2]", id="list"),
        pytest.param((1, 2), "(1, 2)", id="tuple"),
    ],
)
def test_non_referencable_sequences_render_their_value_each_time(
    child: object,
    expected: str,
    render_plain: RenderText,
) -> None:
    rendered = render_plain({"left": child, "right": child}, width=120)

    assert rendered == f"{{'left': {expected}, 'right': {expected}}}"
