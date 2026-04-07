from __future__ import annotations

import pytest

from liblaf.pretty._conf import PrettyKwargs

from ._helpers import render_plain


@pytest.mark.parametrize(
    ("obj", "expected"),
    [
        pytest.param({"a": [1, 2, 3]}, "{'a': [1, 2, 3]}", id="dict"),
        pytest.param([1, "two", None], "[1, 'two', None]", id="list"),
        pytest.param((1, 2, 3), "(1, 2, 3)", id="tuple"),
        pytest.param((1,), "(1,)", id="single-item-tuple"),
        pytest.param({1, 2, 3}, "{1, 2, 3}", id="set"),
        pytest.param(set(), "set()", id="empty-set"),
        pytest.param(
            frozenset({1, 2, 3}),
            "frozenset({1, 2, 3})",
            id="frozenset",
        ),
        pytest.param(frozenset(), "frozenset()", id="empty-frozenset"),
    ],
)
def test_builtin_containers_render_current_output(obj: object, expected: str) -> None:
    assert render_plain(obj) == expected


@pytest.mark.parametrize(
    ("obj", "kwargs", "expected"),
    [
        pytest.param([1, 2, 3, 4], {"max_list": 2}, "[1, 2, ...]", id="max-list"),
        pytest.param(
            {"a": 1, "b": 2, "c": 3},
            {"max_dict": 2},
            "{'a': 1, 'b': 2, ...}",
            id="max-dict",
        ),
        pytest.param(
            {"a": {"b": {"c": 1}}},
            {"max_level": 2},
            "{'a': {'b': {...}}}",
            id="max-level",
        ),
        pytest.param(
            "abcdefghijklmnopqrstuvwxyz0123456789",
            {"max_string": 10},
            "'ab...789'",
            id="max-string",
        ),
        pytest.param(
            10**60,
            {"max_long": 10},
            "100...0000",
            id="max-long",
        ),
    ],
)
def test_repr_limits_render_current_output(
    obj: object,
    kwargs: PrettyKwargs,
    expected: str,
) -> None:
    assert render_plain(obj, **kwargs) == expected
