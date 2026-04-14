"""Base classes for lowered renderables."""

import abc
from collections.abc import Iterable

import attrs
from rich.console import Console, ConsoleOptions, RenderResult

from ._context import CompileContext
from ._layout import Layout, choose_layout


@attrs.frozen
class Lowered(abc.ABC):
    """Renderable output node produced by the pretty-print pipeline."""

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        ctx: CompileContext = CompileContext(console, options)
        return self.render(ctx)

    @abc.abstractmethod
    def layouts(self) -> Iterable[Layout]: ...

    def render(self, ctx: CompileContext) -> RenderResult:
        layout: Layout = choose_layout(self.layouts(), ctx)
        return layout.render(ctx)

    def to_plain(self, console: Console | None = None, **kwargs) -> str:
        """Render this node to deterministic plain text.

        Args:
            console: Optional console to render through. When omitted, a
                plain, no-color Rich console is created.
            **kwargs: Extra keyword arguments forwarded to `Console.print()`.

        Returns:
            The rendered plain-text result.
        """
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
