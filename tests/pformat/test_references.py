from typing import Any

from liblaf.pretty import PrettyBuilder, PrettySpec, pformat


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


def test_shallowest_anchor() -> None:
    item: list[Any] = []
    obj: list[object] = [[item], item]
    item_id: int = id(item)
    assert (
        pformat(obj)
        == f"""\
[
│   [<*list object at {item_id:#x}>],
│   []  # <*list object at {item_id:#x}>
]
"""
    )


class InlineRepeat:
    def __liblaf_pretty__(self, builder: PrettyBuilder) -> PrettySpec:
        return builder.object([builder.field("value", "x")], referable=False)


def test_nonreferable_repeat_inlines() -> None:
    obj: InlineRepeat = InlineRepeat()
    assert pformat([obj, obj]) == "[InlineRepeat(value='x'), InlineRepeat(value='x')]\n"


class NonreferableCycle:
    child: "NonreferableCycle"

    def __init__(self) -> None:
        self.child = self

    def __liblaf_pretty__(self, builder: PrettyBuilder) -> PrettySpec:
        return builder.object([builder.field("child", self.child)], referable=False)


def test_nonreferable_cycle_uses_reference() -> None:
    obj = NonreferableCycle()
    obj_id: int = id(obj)
    assert (
        pformat(obj)
        == f"NonreferableCycle(child=<*NonreferableCycle object at {obj_id:#x}>)\n"
    )
