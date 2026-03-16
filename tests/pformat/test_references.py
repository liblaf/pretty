from typing import Any

from liblaf.pretty import pformat


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
