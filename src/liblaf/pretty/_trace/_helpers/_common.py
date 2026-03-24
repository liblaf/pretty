from __future__ import annotations

from rich.text import Text


def copy_text(value: str | Text) -> Text:
    if isinstance(value, Text):
        return value.copy()
    return Text(value)


type PrettyChild = object
