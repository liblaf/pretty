from __future__ import annotations

import io
import re

import attrs
from rich.console import Console

from liblaf.pretty import pformat, pprint


def render_to_plain(obj: object, /, *, width: int = 80, **kwargs: object) -> str:
    console = Console(width=width, color_system=None, soft_wrap=True)
    return pformat(obj, **kwargs).to_plain(console)


def render_with_pprint(obj: object, /, *, width: int = 80, **kwargs: object) -> str:
    buffer = io.StringIO()
    console = Console(file=buffer, width=width, color_system=None, soft_wrap=True)
    pprint(obj, console=console, **kwargs)
    return buffer.getvalue()


def test_pformat_returns_width_aware_plain_text() -> None:
    assert render_to_plain({"alpha": [1, 2, 3]}, width=12) == (
        "{\n|   'alpha': [\n|   |   1,\n|   |   2, 3\n|   ]\n}"
    )


def test_pprint_writes_to_the_provided_console() -> None:
    assert render_with_pprint({"alpha": [1, 2, 3]}, width=12) == (
        "{\n|   'alpha': [\n|   |   1,\n|   |   2, 3\n|   ]\n}"
    )


def test_hide_defaults_can_be_overridden_per_call() -> None:
    @attrs.define
    class Point:
        x: int = 1
        y: int = 2

    assert render_to_plain(Point()) == "Point()"
    assert render_to_plain(Point(), hide_defaults=False) == "Point(x=1, y=2)"


def test_max_dict_truncates_after_the_configured_limit() -> None:
    assert render_to_plain({"a": 1, "b": 2, "c": 3}, max_dict=2) == (
        "{'a': 1, 'b': 2, ...}"
    )


def test_shared_references_are_annotated_for_referencable_objects() -> None:
    child = {"x": 1}

    rendered = render_to_plain({"left": child, "right": child}, width=120)

    match = re.search(
        r"'left': \{'x': 1\},  # <dict @ ([0-9a-f]+)>\n\|   'right': <dict @ \1>",
        rendered,
    )
    assert match is not None
