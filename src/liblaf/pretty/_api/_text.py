from rich.text import Text


def has_ansi(text: str) -> bool:
    return "\x1b" in text


def text(text: str) -> Text:
    if has_ansi(text):
        return Text.from_ansi(text)
    return Text.from_markup(text)
