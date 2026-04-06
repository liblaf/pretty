from rich.text import Text


def as_text(text: str | Text) -> Text:
    if isinstance(text, Text):
        return text
    if has_ansi(text):
        return Text.from_ansi(text)
    return Text.from_markup(text)


def has_ansi(text: str) -> bool:
    return "\x1b" in text
