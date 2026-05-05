from __future__ import annotations

from collections.abc import Callable
from typing import Any

from rich.text import Text

from liblaf.pretty.custom import PrettyContext

type NormalizeRefs = Callable[[str], str]
type RenderText = Callable[..., str]


class MultilineValue:
    def __pretty__(self, ctx: PrettyContext) -> Any:
        return ctx.leaf(self, Text("alpha\nbeta"))


class InlineValue:
    def __pretty__(self, ctx: PrettyContext) -> Any:
        return ctx.leaf(self, Text("leaf"))


class SharedKey:
    def __hash__(self) -> int:
        return id(self)

    def __pretty__(self, ctx: PrettyContext) -> Any:
        return ctx.leaf(self, Text("key"))


def test_multiline_leaf_values_render_inside_sequence(
    render_plain: RenderText,
) -> None:
    assert render_plain([MultilineValue()], width=120) == "[\n|   alpha\n|   beta\n]"


def test_multiline_shared_leaf_annotations_stay_on_the_first_line(
    render_plain: RenderText,
    normalize_refs: NormalizeRefs,
) -> None:
    value = MultilineValue()

    rendered = normalize_refs(render_plain({"left": value, "right": value}, width=120))

    assert rendered == (
        "{\n"
        "|   'left': alpha  # <MultilineValue @ <id>>\n"
        "|   beta,\n"
        "|   'right': <MultilineValue @ <id>>\n"
        "}"
    )


def test_shared_leaf_annotations_render_for_positional_items(
    render_plain: RenderText,
    normalize_refs: NormalizeRefs,
) -> None:
    value = InlineValue()

    rendered = normalize_refs(render_plain([value, value], width=120))

    assert rendered == (
        "[\n|   leaf,  # <InlineValue @ <id>>\n|   <InlineValue @ <id>>\n]"
    )


def test_referenced_mapping_key_annotation_renders_above_the_key(
    render_plain: RenderText,
    normalize_refs: NormalizeRefs,
) -> None:
    key = SharedKey()

    rendered = normalize_refs(render_plain({key: "first", "after": key}, width=120))

    assert rendered == (
        "{\n"
        "|   # <SharedKey @ <id>>\n"
        "|   key: 'first',\n"
        "|   'after': <SharedKey @ <id>>\n"
        "}"
    )


def test_referenced_mapping_key_annotation_precedes_multiline_values(
    render_plain: RenderText,
    normalize_refs: NormalizeRefs,
) -> None:
    key = SharedKey()

    rendered = normalize_refs(
        render_plain({key: MultilineValue(), "after": key}, width=120)
    )

    assert rendered == (
        "{\n"
        "|   # <SharedKey @ <id>>\n"
        "|   key: alpha\n"
        "|   beta,\n"
        "|   'after': <SharedKey @ <id>>\n"
        "}"
    )


def test_multiline_mapping_keys_render_before_flat_values(
    render_plain: RenderText,
) -> None:
    assert render_plain({MultilineValue(): "value"}, width=120) == (
        "{\n|   alpha\n|   beta: 'value'\n}"
    )


def test_multiline_mapping_keys_and_values_render_around_the_separator(
    render_plain: RenderText,
) -> None:
    assert render_plain({MultilineValue(): MultilineValue()}, width=120) == (
        "{\n|   alpha\n|   beta: alpha\n|   beta\n}"
    )
