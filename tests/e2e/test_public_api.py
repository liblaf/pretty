from __future__ import annotations

import io
from collections.abc import Callable

import attrs
import pytest
import rich
from rich.console import Console

from liblaf.pretty import pformat, pp, pprint

type RenderText = Callable[..., str]

EXPECTED_WRAPPED_MAPPING = "{\n|   'alpha': [\n|   |   1,\n|   |   2, 3\n|   ]\n}"


def test_pformat_returns_width_aware_plain_text(render_plain: RenderText) -> None:
    assert render_plain({"alpha": [1, 2, 3]}, width=12) == EXPECTED_WRAPPED_MAPPING


def test_pprint_writes_to_the_provided_console(render_pprint: RenderText) -> None:
    assert render_pprint({"alpha": [1, 2, 3]}, width=12) == EXPECTED_WRAPPED_MAPPING


def test_pprint_uses_the_active_rich_console_when_omitted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    buffer = io.StringIO()
    console = Console(
        file=buffer,
        width=12,
        color_system=None,
        soft_wrap=True,
        no_color=True,
        markup=False,
        emoji=False,
        highlight=False,
    )
    monkeypatch.setattr(rich, "get_console", lambda: console)

    pprint({"alpha": [1, 2, 3]})

    assert buffer.getvalue() == EXPECTED_WRAPPED_MAPPING


def test_pp_is_an_alias_of_pprint() -> None:
    assert pp is pprint


def test_to_plain_uses_a_safe_default_console() -> None:
    assert pformat("[bold]x[/]").to_plain() == "'[bold]x[/]'"


def test_hide_defaults_can_be_overridden_per_call(render_plain: RenderText) -> None:
    @attrs.define
    class Point:
        x: int = 1
        y: int = 2

    assert render_plain(Point()) == "Point()"
    assert render_plain(Point(), hide_defaults=False) == "Point(x=1, y=2)"


def test_max_dict_truncates_after_the_configured_limit(
    render_plain: RenderText,
) -> None:
    assert render_plain({"a": 1, "b": 2, "c": 3}, max_dict=2) == (
        "{'a': 1, 'b': 2, ...}"
    )


def test_max_list_truncates_after_the_configured_limit(
    render_plain: RenderText,
) -> None:
    assert render_plain([1, 2, 3], max_list=2) == "[1, 2, ...]"
