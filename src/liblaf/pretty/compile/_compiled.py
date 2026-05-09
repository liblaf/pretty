import functools
from collections import UserList
from collections.abc import Iterable, Sequence
from typing import Self

import attrs
from rich.console import Console, ConsoleOptions, RenderResult
from rich.segment import Segment


class Segments(UserList[Segment]):
    @functools.cached_property
    def width(self) -> int:
        return sum(segment.cell_length for segment in self.data)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield from self.data


@attrs.frozen
class Compiled:
    lines: Sequence[Segments] = attrs.field(factory=list)
    newline: bool = attrs.field(default=False, kw_only=True)
    break_after: bool = attrs.field(default=False, kw_only=True)
    break_before: bool = attrs.field(default=False, kw_only=True)

    @functools.cached_property
    def height(self) -> int:
        return len(self.lines)

    @functools.cached_property
    def width(self) -> int:
        return max(line.width for line in self.lines)

    @classmethod
    def from_segments(
        cls,
        segments: Iterable[Segment],
        *,
        break_after: bool = False,
        break_before: bool = False,
    ) -> Self:
        lines: list[Segments] = []
        newline: bool = False
        for line, newline in Segment.split_lines_terminator(segments):  # noqa: B007
            lines.append(Segments(line))
        return cls(
            lines=lines,
            newline=newline,
            break_after=break_after,
            break_before=break_before,
        )

    def __add__(self, other: Segment | Iterable[Segment] | Self) -> Self:
        if isinstance(other, Segment):
            other: Self = self.from_segments([other])
        elif isinstance(other, Iterable) and not isinstance(other, Compiled):
            other: Self = self.from_segments(other)
        assert self.joinable(other)
        if self.newline:
            lines: Sequence[Segments] = [*self.lines, *other.lines]
        else:
            lines: Sequence[Segments] = [
                *self.lines[:-1],
                self.lines[-1] + other.lines[0],
                *other.lines[1:],
            ]
        return attrs.evolve(
            self,
            lines=lines,
            newline=other.newline,
            break_after=other.break_after,
            break_before=self.break_before,
        )

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        newline: Segment = Segment.line()
        for i, line in enumerate(self.lines):
            yield from line
            if i < len(self.lines) - 1 or self.newline:
                yield newline

    def indent(self, indent: Iterable[Segment]) -> Self:
        indent: Segments = Segments(indent)
        return attrs.evolve(self, lines=[indent + line for line in self.lines])

    def joinable(self, other: Self) -> bool:
        return self.newline or not (self.break_after or other.break_before)
