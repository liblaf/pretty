from __future__ import annotations

import logging
import sys
import types
from typing import Any

import pytest
from rich.console import Console
from rich.text import Text

from liblaf.pretty import PrettyOptions
from liblaf.pretty.custom import PrettyContext, PrettyRegistry


def default_options() -> PrettyOptions:
    return PrettyOptions(
        max_level=6,
        max_list=6,
        max_array=5,
        max_dict=4,
        max_string=30,
        max_long=40,
        max_other=30,
        indent=Text("|   ", "repr.indent"),
        hide_defaults=True,
    )


def render_with_registry(
    obj: object, /, *, registry: PrettyRegistry, width: int = 80
) -> str:
    console = Console(
        width=width,
        color_system=None,
        soft_wrap=True,
        no_color=True,
        markup=False,
        emoji=False,
        highlight=False,
    )
    ctx = PrettyContext(options=default_options(), registry=registry)
    lowered = ctx.trace(ctx.wrap_lazy(obj)).lower(ctx.finish())
    return lowered.to_plain(console=console)


def test_registry_prefers_dunder_pretty_over_registered_handlers() -> None:
    registry = PrettyRegistry()

    class Sample:
        def __pretty__(self, ctx: PrettyContext) -> Any:
            return ctx.leaf(self, Text("method", "repr.tag_name"), referencable=False)

    @registry.register_type(Sample)
    def _type_handler(obj: Sample, ctx: PrettyContext) -> Any:
        return ctx.leaf(obj, Text("type", "repr.tag_name"), referencable=False)

    @registry.register_func
    def _func_handler(obj: Any, ctx: PrettyContext) -> Any:
        if not isinstance(obj, Sample):
            return None
        return ctx.leaf(obj, Text("func", "repr.tag_name"), referencable=False)

    assert render_with_registry(Sample(), registry=registry) == "method"


def test_registry_prefers_type_handlers_over_structural_handlers() -> None:
    registry = PrettyRegistry()

    class Sample:
        pass

    @registry.register_type(Sample)
    def _type_handler(obj: Sample, ctx: PrettyContext) -> Any:
        return ctx.leaf(obj, Text("type", "repr.tag_name"), referencable=False)

    @registry.register_func
    def _func_handler(obj: Any, ctx: PrettyContext) -> Any:
        if not isinstance(obj, Sample):
            return None
        return ctx.leaf(obj, Text("func", "repr.tag_name"), referencable=False)

    assert render_with_registry(Sample(), registry=registry) == "type"


def test_later_structural_registration_wins() -> None:
    registry = PrettyRegistry()

    class Sample:
        pass

    @registry.register_func
    def _first(obj: Any, ctx: PrettyContext) -> Any:
        if not isinstance(obj, Sample):
            return None
        return ctx.leaf(obj, Text("first", "repr.tag_name"), referencable=False)

    @registry.register_func
    def _second(obj: Any, ctx: PrettyContext) -> Any:
        if not isinstance(obj, Sample):
            return None
        return ctx.leaf(obj, Text("second", "repr.tag_name"), referencable=False)

    assert render_with_registry(Sample(), registry=registry) == "second"


def test_resolve_lazy_removes_missing_targets_after_logging(
    caplog: pytest.LogCaptureFixture,
) -> None:
    module_name = "_pretty_missing_example"
    registry = PrettyRegistry()
    module = types.ModuleType(module_name)

    @registry.register_lazy(module_name, "MissingValue")
    def _pretty_missing(obj: Any, ctx: PrettyContext) -> Any:
        return ctx.leaf(obj, Text("missing", "repr.tag_name"), referencable=False)

    sys.modules[module_name] = module
    try:
        with caplog.at_level(logging.ERROR, logger="liblaf.pretty.custom._registry"):
            registry.resolve_lazy()
    finally:
        del sys.modules[module_name]

    assert not registry.lazy_handlers
    assert any(record.exc_info is not None for record in caplog.records)
