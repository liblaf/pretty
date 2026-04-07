from __future__ import annotations

import pytest

from ._helpers import render_plain


@pytest.mark.parametrize(
    ("width", "expected"),
    [
        pytest.param(
            10,
            "{\n|   'alpha': [\n|   |   1,\n|   |   2,\n|   |   3\n|   ]\n}",
            id="width-10",
        ),
        pytest.param(
            12,
            "{\n|   'alpha': [\n|   |   1,\n|   |   2, 3\n|   ]\n}",
            id="width-12",
        ),
        pytest.param(
            16,
            "{\n|   'alpha': [\n|   |   1, 2, 3\n|   ]\n}",
            id="width-16",
        ),
        pytest.param(20, "{'alpha': [1, 2, 3]}", id="width-20"),
    ],
)
def test_to_plain_breakpoints_follow_console_width(width: int, expected: str) -> None:
    assert render_plain({"alpha": [1, 2, 3]}, width=width) == expected
