import abc

import attrs
from rich.console import Console, ConsoleOptions, RenderResult

from ._writer import Writer


@attrs.frozen
class Lowered(abc.ABC):
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        writer: Writer = Writer(console, options)
        yield from self.render(writer)

    @abc.abstractmethod
    def render(self, writer: Writer) -> RenderResult: ...

    def to_plain(self, console: Console | None = None) -> str:
        if console is None:
            console: Console = Console(color_system=None, soft_wrap=True)
        with console.capture() as capture:
            console.print(self)
        return capture.get()
