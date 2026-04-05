from collections.abc import Iterable
from typing import Any

import attrs
from rich.text import Text

from liblaf.pretty import (
    PrettyOptions,
    SpecContainer,
    SpecField,
    SpecLeaf,
    pformat,
)


def test_recursive() -> None:
    obj: list[object] = []
    obj.append(obj)
    obj_id: int = id(obj)
    assert (
        pformat(obj)
        == f"[<*list object at {obj_id:#x}>]  # <*list object at {obj_id:#x}>\n"
    )


def test_sibling() -> None:
    item: list[Any] = []
    obj: list[list[Any]] = [item, item]
    item_id: int = id(item)
    assert (
        pformat(obj)
        == f"""\
[
│   [],  # <*list object at {item_id:#x}>
│   <*list object at {item_id:#x}>
]
"""
    )


def test_shallowest_first_reference() -> None:
    shared: list[Any] = []
    obj: list[Any] = [[shared], shared]
    shared_id: int = id(shared)
    assert (
        pformat(obj)
        == f"""\
[
│   [<*list object at {shared_id:#x}>],
│   []  # <*list object at {shared_id:#x}>
]
"""
    )


@attrs.define
class CountingPretty:
    calls: int = 0
    spec: "CountingSpec" = attrs.field(init=False)

    def __attrs_post_init__(self) -> None:
        self.spec = CountingSpec(
            cls=type(self),
            id_=id(self),
            referable=True,
            begin=Text.assemble(
                ("CountingPretty", "repr.tag_name"), ("(", "repr.tag_start")
            ),
            end=Text(")", "repr.tag_end"),
            owner=self,
        )

    def __pretty__(self, _options: PrettyOptions) -> "CountingSpec":
        return self.spec


@attrs.frozen(slots=True, kw_only=True)
class CountingSpec(SpecContainer):
    owner: CountingPretty

    def iter_children(self) -> Iterable[SpecField]:
        self.owner.calls += 1
        yield SpecField(
            name="value",
            value=SpecLeaf(cls=int, referable=False, text=Text("1", "repr.number")),
        )


def test_canonical_container_is_expanded_once() -> None:
    shared = CountingPretty()
    assert "<*CountingPretty object at " in pformat([shared, shared])
    assert shared.calls == 1


@attrs.define
class NonReferablePretty:
    spec: SpecLeaf = attrs.field(init=False)

    def __attrs_post_init__(self) -> None:
        self.spec = SpecLeaf(
            cls=type(self),
            id_=id(self),
            referable=False,
            text=Text("CUSTOM"),
        )

    def __pretty__(self, _options: PrettyOptions) -> SpecLeaf:
        return self.spec


def test_nonreferable_nodes_never_collapse() -> None:
    shared = NonReferablePretty()
    assert pformat([shared, shared]) == "[CUSTOM, CUSTOM]\n"
