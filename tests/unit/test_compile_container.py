from __future__ import annotations

import attrs
from rich.console import RenderResult
from rich.text import Text

from liblaf.pretty.compile._base import RenderContext
from liblaf.pretty.compile._container import (
    CompiledContainerBreakCommentAfter,
    CompiledContainerBreakCommentBefore,
    CompiledContainerBreakNoComment,
    CompiledContainerFlatCommentAfter,
    CompiledContainerFlatCommentBefore,
    CompiledContainerFlatNoComment,
)


@attrs.frozen
class DummyDoc:
    width: int
    n_lines: int
    first_line_width: int
    last_line_width: int
    has_leading_comment: bool = False
    has_trailing_comment: bool = False

    def render(self, _ctx: RenderContext) -> RenderResult:
        yield from ()


def test_flat_container_metrics_use_display_width() -> None:
    doc = DummyDoc(width=3, n_lines=1, first_line_width=3, last_line_width=3)

    compiled = CompiledContainerFlatCommentAfter(
        begin=Text("["),
        doc=doc,
        end=Text("]"),
        comment=Text("表"),
    )

    assert compiled.width == 9
    assert compiled.n_lines == 1
    assert compiled.first_line_width == 9
    assert compiled.last_line_width == 9
    assert compiled.has_leading_comment is False
    assert compiled.has_trailing_comment is True


def test_flat_container_metrics_wrap_multiline_child() -> None:
    doc = DummyDoc(width=10, n_lines=3, first_line_width=4, last_line_width=5)

    no_comment = CompiledContainerFlatNoComment(Text("["), doc, Text("]"))
    before = CompiledContainerFlatCommentBefore(
        begin=Text("["),
        doc=doc,
        end=Text("]"),
        comment=Text("# before"),
    )
    after = CompiledContainerFlatCommentAfter(
        begin=Text("["),
        doc=doc,
        end=Text("]"),
        comment=Text("# after"),
    )

    assert (
        no_comment.width,
        no_comment.n_lines,
        no_comment.first_line_width,
        no_comment.last_line_width,
    ) == (10, 3, 5, 6)
    assert (
        before.width,
        before.n_lines,
        before.first_line_width,
        before.last_line_width,
        before.has_leading_comment,
        before.has_trailing_comment,
    ) == (10, 4, 8, 6, True, False)
    assert (
        after.width,
        after.n_lines,
        after.first_line_width,
        after.last_line_width,
        after.has_leading_comment,
        after.has_trailing_comment,
    ) == (15, 3, 5, 15, False, True)


def test_break_container_metrics_include_indented_child_width() -> None:
    doc = DummyDoc(width=7, n_lines=2, first_line_width=2, last_line_width=7)

    no_comment = CompiledContainerBreakNoComment(
        begin=Text("["),
        doc=doc,
        end=Text("]"),
        indent=Text("  "),
    )
    before = CompiledContainerBreakCommentBefore(
        begin=Text("["),
        doc=doc,
        end=Text("]"),
        indent=Text("  "),
        comment=Text("# before"),
    )
    after = CompiledContainerBreakCommentAfter(
        begin=Text("["),
        doc=doc,
        end=Text("]"),
        indent=Text("  "),
        comment=Text("# after"),
    )

    assert (
        no_comment.width,
        no_comment.n_lines,
        no_comment.first_line_width,
        no_comment.last_line_width,
    ) == (9, 4, 1, 1)
    assert (
        before.width,
        before.n_lines,
        before.first_line_width,
        before.last_line_width,
        before.has_leading_comment,
        before.has_trailing_comment,
    ) == (9, 5, 8, 1, True, False)
    assert (
        after.width,
        after.n_lines,
        after.first_line_width,
        after.last_line_width,
        after.has_leading_comment,
        after.has_trailing_comment,
    ) == (10, 4, 10, 1, False, True)
