from collections.abc import Generator
from typing import override

import attrs
from rich.segment import Segment
from rich.text import Text

from liblaf.pretty.compile import Compiled, Constraints, Flags
from liblaf.pretty.literals import COMMENT_GAP

from ._base import Layout, Lowered
from ._comment import CommentLayout
from ._context import CompileContext


class Container(Lowered):
    begin: Text
    doc: Lowered
    end: Text
    indent: Text
    comment: Text

    @override
    def layouts(self) -> Generator[Layout]:
        for comment_layout in CommentLayout.filter_layouts(self.comment):
            yield ContainerFlat(self, comment_layout)
            yield ContainerBreak(self, comment_layout)


@attrs.frozen
class ContainerFlat(Layout):
    wrapped: Container
    comment_layout: CommentLayout

    @override
    def compile(self, ctx: CompileContext) -> Compiled:
        match self.comment_layout:
            case CommentLayout.NONE:
                begin: Compiled = ctx.compile(self.wrapped.begin)
                end: Compiled = ctx.compile(self.wrapped.end)
            case CommentLayout.AFTER:
                begin: Compiled = ctx.compile(self.wrapped.begin)
                end: Compiled = ctx.compile(
                    self.wrapped.end,
                    COMMENT_GAP,
                    self.wrapped.comment,
                    break_after=True,
                )
            case CommentLayout.BEFORE:
                begin: Compiled = ctx.compile(
                    self.wrapped.comment, "\n", self.wrapped.begin, break_before=True
                )
                end: Compiled = ctx.compile(self.wrapped.end)
        for layout in self.wrapped.doc.filter_layouts(Constraints.INLINE):
            doc: Compiled = layout.compile(ctx)
            compiled: Compiled = begin + doc + end
            if ctx.fits(compiled):
                return compiled
        return compiled

    @override
    def flags(self) -> Flags:
        match self.comment_layout:
            case CommentLayout.NONE:
                return Flags(multiline=False)
            case CommentLayout.AFTER:
                return Flags(multiline=False, break_after=True)
            case CommentLayout.BEFORE:
                return Flags(multiline=False, break_before=True)

    @override
    def satisfies(self, constraints: Constraints) -> bool:
        return super().satisfies(constraints) and self.wrapped.doc.satisfies(
            Constraints.INLINE
        )


@attrs.frozen
class ContainerBreak(Layout):
    wrapped: Container
    comment_layout: CommentLayout

    @override
    def compile(self, ctx: CompileContext) -> Compiled:
        match self.comment_layout:
            case CommentLayout.NONE:
                begin: Compiled = ctx.compile(self.wrapped.begin, "\n")
                end: Compiled = ctx.compile("\n", self.wrapped.end)
            case CommentLayout.AFTER:
                begin: Compiled = ctx.compile(
                    self.wrapped.begin,
                    COMMENT_GAP,
                    self.wrapped.comment,
                    "\n",
                )
                end: Compiled = ctx.compile("\n", self.wrapped.end)
            case CommentLayout.BEFORE:
                begin: Compiled = ctx.compile(
                    self.wrapped.comment, "\n", self.wrapped.begin, break_before=True
                )
                end: Compiled = ctx.compile("\n", self.wrapped.end)
        indent: list[Segment] = list(ctx.render(self.wrapped.indent))
        for layout in self.wrapped.doc.filter_layouts(Constraints.BLOCK):
            doc: Compiled = layout.compile(ctx)
            compiled: Compiled = begin + doc.indent(indent) + end
            if ctx.fits(compiled):
                return compiled
        return compiled

    @override
    def flags(self) -> Flags:
        match self.comment_layout:
            case CommentLayout.NONE | CommentLayout.AFTER:
                return Flags(multiline=True)
            case CommentLayout.BEFORE:
                return Flags(multiline=True, break_before=True)

    @override
    def satisfies(self, constraints: Constraints) -> bool:
        return super().satisfies(constraints) and self.wrapped.doc.satisfies(
            Constraints.BLOCK
        )
