import abc

import attrs
from rich.console import Console, ConsoleOptions, RenderResult

from ._renderer import Renderer


@attrs.frozen
class Lowered(abc.ABC):
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        renderer: Renderer = Renderer(console, options)
        yield from self.render(renderer)

    @abc.abstractmethod
    def render(self, renderer: Renderer) -> RenderResult: ...

    def to_plain(self, console: Console | None = None, **kwargs) -> str:
        if console is None:
            console: Console = Console(
                color_system=None,
                soft_wrap=True,
                no_color=True,
                markup=False,
                emoji=False,
                highlight=False,
            )
        kwargs.setdefault("soft_wrap", True)
        with console.capture() as capture:
            console.print(self, **kwargs)
        return capture.get()
