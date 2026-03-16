from liblaf.pretty import pformat


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
    assert pformat({1, 2}) == "{1, 2}\n"


def test_frozenset() -> None:
    assert pformat(frozenset({1, 2})) == "frozenset({1, 2})\n"


def test_nested() -> None:
    assert (
        pformat({"a": [1, 2, 3]}, max_width=13)
        == """\
{
│   'a': [
│   │   1, 2,
│   │   3
│   ]
}
"""
    )
