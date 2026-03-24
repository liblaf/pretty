import contextlib
import contextvars
from collections.abc import Generator, Mapping
from typing import Any

import environs
from rich.text import Text

from liblaf.pretty._trace._helpers._text import text

env = environs.Env(prefix="LIBLAF_PRETTY_")


class ConfigField[T]:
    var: contextvars.ContextVar[T]

    def __init__(self, name: str, default: T) -> None:
        self.var = contextvars.ContextVar(name, default=default)

    @property
    def name(self) -> str:
        return self.var.name

    def from_options(self, options: Mapping[str, Any] | None = None) -> T:
        if options is not None and (value := options.get(self.name)) is not None:
            return value
        return self.var.get()

    def from_value(self, value: T | None = None) -> T:
        if value is not None:
            return value
        return self.var.get()

    def get(self) -> T:
        return self.var.get()

    def set(self, value: T) -> contextvars.Token[T]:
        return self.var.set(value)

    @contextlib.contextmanager
    def override(self, value: T) -> Generator[T]:
        token: contextvars.Token[T] = self.var.set(value)
        try:
            yield value
        finally:
            self.var.reset(token)


class BoolField(ConfigField[bool]):
    def __init__(self, name: str, default: bool) -> None:  # noqa: FBT001
        default: bool = env.bool(name.upper(), default)
        super().__init__(name, default)


class IntField(ConfigField[int]):
    def __init__(self, name: str, default: int) -> None:
        default: int = env.int(name.upper(), default)
        super().__init__(name, default)


class StrField(ConfigField[str]):
    def __init__(self, name: str, default: str) -> None:
        default: str = env.str(name.upper(), default)
        super().__init__(name, default)


class TextField(ConfigField[Text]):
    def __init__(self, name: str, default: Text) -> None:
        if (value := env.str(name.upper(), None)) is not None:
            default = text(value)
        super().__init__(name, default)
