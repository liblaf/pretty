from __future__ import annotations

from collections.abc import Iterator

import attrs
from rich.repr import RichReprResult

from liblaf.pretty import DescribeContext
from liblaf.pretty._spec import SpecItem, SpecNode

from ._helpers import render_plain


@attrs.frozen
class Demo:
    value: int = 1
    hidden: int = attrs.field(default=2, repr=False)


class RichThing:
    def __rich_repr__(self) -> RichReprResult:
        yield "name", "x"
        yield "skip", 1, 1
        yield "keep", 2, 0
        yield 3


class Greeting:
    def __pretty__(self, ctx: DescribeContext, depth: int) -> SpecNode:
        del depth
        return ctx.container(
            begin="(",
            end=")",
            children=(ctx.name_value("message", "hello"),),
            referencable=False,
            obj=self,
        )


class Leafy:
    def __pretty__(self, ctx: DescribeContext, depth: int) -> SpecNode:
        del depth
        return ctx.leaf("leaf", obj=self, referencable=False)


class LazyChildren:
    def __init__(self, events: list[str]) -> None:
        self.events = events

    def __pretty__(self, ctx: DescribeContext, depth: int) -> SpecNode:
        del depth

        def children() -> Iterator[SpecItem]:
            self.events.append("iterated")
            yield ctx.positional(1)
            yield ctx.name_value("a", 2)
            yield ctx.key_value("b", 3)

        self.events.append("before-container")
        container = ctx.container(
            begin="(",
            end=")",
            children=children(),
            referencable=False,
            obj=self,
        )
        self.events.append("after-container")
        return container


def _repr_thing_a(_self: object) -> str:
    return "ThingA()"


def _repr_thing_b(_self: object) -> str:
    return "ThingB()"


ThingA = type(
    "Thing",
    (),
    {"__module__": "pkg_a", "__repr__": _repr_thing_a},
)
ThingB = type(
    "Thing",
    (),
    {"__module__": "pkg_b", "__repr__": _repr_thing_b},
)


def test_attrs_fieldz_hides_defaults_by_default() -> None:
    assert render_plain(Demo()) == "Demo()"


def test_attrs_fieldz_shows_defaults_when_requested() -> None:
    assert render_plain(Demo(), hide_defaults=False) == "Demo(value=1)"


def test_attrs_fieldz_omits_repr_false_fields_even_when_non_default() -> None:
    assert render_plain(Demo(value=3, hidden=5), hide_defaults=False) == "Demo(value=3)"


def test_rich_repr_skips_default_triplets() -> None:
    assert render_plain(RichThing()) == "RichThing(name='x', keep=2, 3)"


def test_custom_pretty_container_helpers_render_clean_output() -> None:
    assert render_plain(Greeting()) == "Greeting(message='hello')"


def test_custom_pretty_leaf_helper_renders_literal() -> None:
    assert render_plain(Leafy()) == "leaf"


def test_custom_pretty_container_children_are_consumed_lazily() -> None:
    events: list[str] = []

    assert render_plain(LazyChildren(events)) == "LazyChildren(1, a=2, 'b': 3)"
    assert events == ["before-container", "after-container", "iterated"]


def test_shared_references_are_annotated_and_reused() -> None:
    shared = [1, 2]

    assert render_plain([shared, shared]) == (
        "[\n|   [1, 2],  # <list @ <id>>\n|   <list @ <id>>\n]"
    )


def test_cycles_render_without_recursing_forever() -> None:
    cyclic: list[object] = []
    cyclic.append(cyclic)

    assert render_plain(cyclic) == "[<list @ <id>>]  # <list @ <id>>"


def test_duplicate_type_names_use_disambiguated_reference_annotations() -> None:
    first = ThingA()
    second = ThingB()

    assert render_plain([first, second, first]) == (
        "[\n"
        "|   ThingA(),  # <pkg_a.Thing @ <id>>\n"
        "|   ThingB(), <pkg_a.Thing @ <id>>\n"
        "]"
    )
