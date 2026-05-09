import functools
from collections.abc import Generator
from typing import override

import attrs
from rich.containers import Lines
from rich.text import Text

from liblaf.pretty.compile import Compiled, Flags
from liblaf.pretty.literals import COMMENT_GAP

from ._base import Layout, Lowered
from ._comment import CommentLayout
from ._context import CompileContext


@attrs.frozen
class LoweredLeaf(Lowered):
    text: Text
    comment: Text

    @functools.cached_property
    def lines(self) -> Lines:
        return self.text.split(include_separator=True, allow_blank=True)

    @override
    def layouts(self) -> Generator[Layout]:
        if len(self.lines) == 1:
            for comment_layout in CommentLayout.filter_layouts(self.comment):
                yield LoweredLeafFlat(self, comment_layout)
        else:
            for comment_layout in CommentLayout.filter_layouts(self.comment):
                yield LoweredLeafBreak(self, comment_layout)


@attrs.frozen
class LoweredLeafFlat(Layout):
    wrapped: LoweredLeaf
    comment_layout: CommentLayout

    @override
    def compile(self, ctx: CompileContext) -> Compiled:
        match self.comment_layout:
            case CommentLayout.NONE:
                return ctx.compile(self.wrapped.text)
            case CommentLayout.AFTER:
                return ctx.compile(
                    self.wrapped.text,
                    COMMENT_GAP,
                    self.wrapped.comment,
                    break_after=True,
                )
            case CommentLayout.BEFORE:
                return ctx.compile(
                    self.wrapped.comment, "\n", self.wrapped.text, break_before=True
                )

    @override
    def flags(self) -> Flags:
        match self.comment_layout:
            case CommentLayout.NONE:
                return Flags(multiline=False)
            case CommentLayout.AFTER:
                return Flags(multiline=False, break_after=True)
            case CommentLayout.BEFORE:
                return Flags(multiline=False, break_before=True)


@attrs.frozen
class LoweredLeafBreak(Layout):
    wrapped: LoweredLeaf
    comment_layout: CommentLayout

    @override
    def compile(self, ctx: CompileContext) -> Compiled:
        match self.comment_layout:
            case CommentLayout.NONE:
                return ctx.compile(self.wrapped.text)
            case CommentLayout.AFTER:
                first_line: Text = self.wrapped.lines[0].copy()
                first_line.rstrip()
                return ctx.compile(
                    first_line,
                    COMMENT_GAP,
                    self.wrapped.comment,
                    "\n",
                    *self.wrapped.lines[1:],
                )
            case CommentLayout.BEFORE:
                return ctx.compile(
                    self.wrapped.comment, "\n", self.wrapped.text, break_before=True
                )

    @override
    def flags(self) -> Flags:
        match self.comment_layout:
            case CommentLayout.NONE | CommentLayout.AFTER:
                return Flags(multiline=True)
            case CommentLayout.BEFORE:
                return Flags(multiline=True, break_before=True)
