from __future__ import annotations

import sys
import types
from typing import Any

import pytest
from rich.console import Console
from rich.text import Text

from liblaf.pretty import pformat, register_func, register_lazy, register_type
from liblaf.pretty.custom import PrettyContext


def render_to_plain(obj: object, /, *, width: int = 80, **kwargs: object) -> str:
    console = Console(width=width, color_system=None, soft_wrap=True)
    return pformat(obj, **kwargs).to_plain(console)


def test_dunder_pretty_formats_owned_types() -> None:
    class PrettyPoint:
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

        def __pretty__(self, ctx: PrettyContext) -> Any:
            return ctx.container(
                obj=self,
                begin=Text("(", "repr.tag_start"),
                children=[ctx.name_value("x", self.x), ctx.name_value("y", self.y)],
                end=Text(")", "repr.tag_end"),
            )

    assert render_to_plain(PrettyPoint(1, 2)) == "PrettyPoint(x=1, y=2)"


def test_register_type_formats_matching_classes() -> None:
    class RegisteredPoint:
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

    @register_type(RegisteredPoint)
    def _pretty_point(obj: RegisteredPoint, ctx: PrettyContext) -> Any:
        return ctx.container(
            obj=obj,
            begin=Text("(", "repr.tag_start"),
            children=[ctx.name_value("x", obj.x), ctx.name_value("y", obj.y)],
            end=Text(")", "repr.tag_end"),
        )

    assert render_to_plain(RegisteredPoint(1, 2)) == "RegisteredPoint(x=1, y=2)"


def test_register_func_can_match_structural_handlers() -> None:
    class Vector:
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

    @register_func
    def _pretty_vector(obj: Any, ctx: PrettyContext) -> Any:
        if not isinstance(obj, Vector):
            return None
        return ctx.container(
            obj=obj,
            begin=Text("<", "repr.tag_start"),
            children=[ctx.positional(obj.x), ctx.positional(obj.y)],
            end=Text(">", "repr.tag_end"),
        )

    assert render_to_plain(Vector(1, 2)) == "Vector<1, 2>"


def test_register_lazy_waits_for_the_target_module(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module_name = "_pretty_lazy_example"
    class_name = "LazyValue"
    module = types.ModuleType(module_name)
    lazy_value_cls = type(
        class_name,
        (),
        {
            "__module__": module_name,
            "__init__": lambda self, value: setattr(self, "value", value),
        },
    )
    module.LazyValue = lazy_value_cls
    value = lazy_value_cls(7)

    @register_lazy(module_name, class_name)
    def _pretty_lazy_value(obj: Any, ctx: PrettyContext) -> Any:
        return ctx.leaf(
            obj, Text(f"LazyValue({obj.value})", "repr.tag_name"), referencable=False
        )

    before_import = render_to_plain(value)
    assert before_import.startswith("<_pretty_lazy")
    assert before_import.endswith(">")
    assert before_import != "LazyValue(7)"

    monkeypatch.setitem(sys.modules, module_name, module)

    assert render_to_plain(value) == "LazyValue(7)"
