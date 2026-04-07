from __future__ import annotations

import re
from typing import Unpack

from rich.console import Console

from liblaf.pretty import pformat
from liblaf.pretty._conf import PrettyKwargs

DEFAULT_PRETTY_KWARGS: PrettyKwargs = {
    "max_level": 6,
    "max_list": 6,
    "max_array": 5,
    "max_dict": 4,
    "max_string": 30,
    "max_long": 40,
    "max_other": 30,
    "indent": "|   ",
    "hide_defaults": True,
}
REF_ID_RE = re.compile(r"(?<=@ )[0-9a-f]+")


def render_plain(
    obj: object,
    *,
    width: int = 80,
    normalize_refs: bool = True,
    **kwargs: Unpack[PrettyKwargs],
) -> str:
    console = Console(width=width, color_system=None, soft_wrap=True)
    text = pformat(obj, **{**DEFAULT_PRETTY_KWARGS, **kwargs}).to_plain(console)
    if normalize_refs:
        text = REF_ID_RE.sub("<id>", text)
    return text
