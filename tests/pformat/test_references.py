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


@attrs.frozen(kw_only=True)
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


class MultilinePretty:
    def __pretty__(self, _options: PrettyOptions) -> SpecLeaf:
        return SpecLeaf(
            cls=type(self),
            id_=id(self),
            referable=True,
            text=Text("line1\nline2"),
        )


def test_multiline_references_keep_first_line_when_annotated() -> None:
    shared = MultilinePretty()
    shared_id: int = id(shared)
    assert (
        pformat([shared, shared], options=PrettyOptions(max_width=200))
        == f"""\
[
│   line1  # <*MultilinePretty object at {shared_id:#x}>
│   line2,
│   <*MultilinePretty object at {shared_id:#x}>
]
"""
    )


def test_annotated_mapping_key_keeps_separator_on_same_line() -> None:
    class KeyPretty:
        def __pretty__(self, _options: PrettyOptions) -> SpecLeaf:
            return SpecLeaf(
                cls=type(self),
                id_=id(self),
                referable=True,
                text=Text("K"),
            )

    shared = KeyPretty()
    shared_id: int = id(shared)
    assert (
        pformat({shared: 1, "other": shared}, options=PrettyOptions(max_width=200))
        == f"""\
{{
│   K: 1,  # <*KeyPretty object at {shared_id:#x}>
│   'other': <*KeyPretty object at {shared_id:#x}>
}}
"""
    )


def test_annotated_container_mapping_key_renders_annotation_after_opening_delimiter() -> (
    None
):
    shared = (1,)
    shared_id: int = id(shared)
    assert (
        pformat({shared: 1, "other": shared}, options=PrettyOptions(max_width=200))
        == f"""\
{{
│   (  # <*tuple object at {shared_id:#x}>
│   │   1,
│   ): 1,
│   'other': <*tuple object at {shared_id:#x}>
}}
"""
    )
