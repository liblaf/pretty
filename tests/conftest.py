from __future__ import annotations

import io
import re
from collections.abc import Callable

import pytest
from rich.console import Console

from liblaf.pretty import pformat, pprint

type NormalizeRefs = Callable[[str], str]
type RenderText = Callable[..., str]


def make_console(*, width: int = 80, file: io.StringIO | None = None) -> Console:
    return Console(
        file=file,
        width=width,
        color_system=None,
        soft_wrap=True,
        no_color=True,
        markup=False,
        emoji=False,
        highlight=False,
    )


@pytest.fixture
def normalize_refs() -> NormalizeRefs:
    def _normalize_refs(text: str) -> str:
        return re.sub(r"@ [0-9a-f]+", "@ <id>", text)

    return _normalize_refs


@pytest.fixture
def render_plain() -> RenderText:
    def _render_plain(obj: object, /, *, width: int = 80, **kwargs: object) -> str:
        return pformat(obj, **kwargs).to_plain(console=make_console(width=width))

    return _render_plain


@pytest.fixture
def render_pprint() -> RenderText:
    def _render_pprint(obj: object, /, *, width: int = 80, **kwargs: object) -> str:
        buffer = io.StringIO()
        pprint(obj, console=make_console(width=width, file=buffer), **kwargs)
        return buffer.getvalue()

    return _render_pprint
