from rich.text import Text

from liblaf.pretty import PrettyOptions, SpecLeaf, pformat


def test_list() -> None:
    assert pformat([]) == "[]\n"
    assert pformat([0]) == "[0]\n"
    assert pformat([0, 1]) == "[0, 1]\n"
    assert pformat([0, 1, 2]) == "[0, 1, 2]\n"


def test_tuple() -> None:
    assert pformat(()) == "()\n"
    assert pformat((0,)) == "(0,)\n"
    assert pformat((0, 1)) == "(0, 1)\n"
    assert pformat((0, 1, 2)) == "(0, 1, 2)\n"


def test_dict() -> None:
    assert pformat({"a": 1, "b": 2}) == "{'a': 1, 'b': 2}\n"


def test_set() -> None:
    assert pformat(set()) == "set()\n"
    assert pformat({1, 2}) == "{1, 2}\n"


def test_frozenset() -> None:
    assert pformat(frozenset()) == "frozenset()\n"
    assert pformat(frozenset({1, 2})) == "frozenset({1, 2})\n"


def test_nested() -> None:
    assert (
        pformat({"a": [1, 2, 3]}, options=PrettyOptions(max_width=13))
        == """\
{
│   'a': [
│   │   1, 2,
│   │   3
│   ]
}
"""
    )


def test_nested_value_keeps_flat_layout_when_it_fits_after_break() -> None:
    assert (
        pformat([0, [1, 2]], options=PrettyOptions(max_width=10))
        == """\
[
│   0,
│   [1, 2]
]
"""
    )


def test_multiline_value_does_not_capture_following_sibling() -> None:
    class Multi:
        def __pretty__(self, _options: PrettyOptions) -> object:
            return SpecLeaf(
                cls=type(self),
                referable=False,
                text=Text("x\ny"),
            )

    assert (
        pformat([Multi(), 2], options=PrettyOptions(max_width=200))
        == """\
[
│   x
│   y,
│   2
]
"""
    )


def test_multiline_mapping_key_does_not_capture_following_items() -> None:
    class Multi:
        def __pretty__(self, _options: PrettyOptions) -> object:
            return SpecLeaf(
                cls=type(self),
                referable=False,
                text=Text("k1\nk2"),
            )

    assert (
        pformat({Multi(): 1, "b": 2}, options=PrettyOptions(max_width=200))
        == """\
{
│   k1
│   k2: 1,
│   'b': 2
}
"""
    )
