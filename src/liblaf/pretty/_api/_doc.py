from rich.console import Console, ConsoleOptions, RenderResult

from .._compile import Lowered


class PrettyDoc:
    def __init__(self, root: Lowered) -> None:
        self._root: Lowered = root

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield from self._root.__rich_console__(console, options)
