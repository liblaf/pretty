from __future__ import annotations

import attrs
from rich.repr import RichReprResult
from rich.text import Text

from liblaf.pretty import DescribeContext
from liblaf.pretty._spec._node import SpecContainer

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
    def __pretty__(self, ctx: DescribeContext, depth: int) -> SpecContainer:
        del depth
        return SpecContainer(
            begin=Text("Greeting("),
            items=ctx.add_separators([ctx.describe_named_item("message", "hello")]),
            end=Text(")"),
            indent=ctx.options.indent,
            ref=ctx.ref(self),
            referencable=False,
        )


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


def test_custom_pretty_current_output() -> None:
    assert render_plain(Greeting()) == "GreetingGreeting(message='hello')"


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
