import logging
import sys
import types
from collections.abc import Iterable

import attrs
import pytest
from rich.console import Console
from rich.text import Text

from liblaf import pretty
from liblaf.pretty import (
    PrettyOptions,
    SpecContainer,
    SpecField,
    SpecLeaf,
    pdoc,
    pformat,
    register_func,
    register_lazy,
    register_type,
)
from liblaf.pretty._describe._registry import DescribeRegistry


def test_public_exports() -> None:
    assert pretty.__all__ == [
        "PrettyOptions",
        "PrettyPrintable",
        "Spec",
        "SpecContainer",
        "SpecField",
        "SpecItem",
        "SpecKeyValue",
        "SpecLeaf",
        "SpecValue",
        "pdoc",
        "pformat",
        "pprint",
        "register_func",
        "register_lazy",
        "register_type",
    ]


def test_pretty_options_defaults() -> None:
    options = PrettyOptions()
    assert options.indent.plain == "│   "
    assert options.max_dict == 4
    assert options.max_level == 6
    assert options.max_list == 6
    assert options.max_long == 40
    assert options.max_other == 30
    assert options.max_string == 30
    assert options.max_width == 88


@attrs.frozen(kw_only=True)
class GreetingSpec(SpecContainer):
    child: SpecLeaf

    def iter_children(self) -> Iterable[SpecField]:
        yield SpecField(name="message", value=self.child)


@attrs.define
class Greeting:
    def __pretty__(self, _options: PrettyOptions) -> GreetingSpec:
        return GreetingSpec(
            cls=type(self),
            id_=id(self),
            referable=True,
            begin=Text.assemble(("Greeting", "repr.tag_name"), ("(", "repr.tag_start")),
            end=Text(")", "repr.tag_end"),
            child=SpecLeaf(
                cls=str,
                referable=False,
                text=Text("'hello'", "repr.str"),
            ),
        )


def test_custom_pretty_protocol() -> None:
    assert pformat(Greeting()) == "Greeting(message='hello')\n"


def test_pdoc_returns_rich_renderable() -> None:
    renderable = pdoc([1, 2])
    console = Console(color_system=None, soft_wrap=True, width=88)
    with console.capture() as capture:
        console.print(renderable)
    assert capture.get() == "[1, 2]\n"


def test_register_type() -> None:
    class RegisteredType:
        pass

    @register_type(RegisteredType)
    def _describe_registered(_obj: RegisteredType, _options: PrettyOptions) -> SpecLeaf:
        return SpecLeaf(cls=RegisteredType, referable=False, text=Text("REGISTERED"))

    assert pformat(RegisteredType()) == "REGISTERED\n"


def test_register_lazy() -> None:
    module_name = "tests.pretty_lazy_describe_module"
    module = types.ModuleType(module_name)
    lazy_cls = type("LazyDescribeType", (), {"__module__": module_name})
    module.__dict__["LazyDescribeType"] = lazy_cls
    sys.modules[module_name] = module

    @register_lazy(module_name, "LazyDescribeType")
    def _describe_lazy(_obj: object, _options: PrettyOptions) -> SpecLeaf:
        return SpecLeaf(cls=lazy_cls, referable=False, text=Text("LAZY"))

    assert pformat(lazy_cls()) == "LAZY\n"


def test_register_func() -> None:
    class FuncRegistered:
        pass

    @register_func
    def _describe_func(obj: object, _options: PrettyOptions) -> SpecLeaf | None:
        if not isinstance(obj, FuncRegistered):
            return None
        return SpecLeaf(cls=FuncRegistered, referable=False, text=Text("FUNC"))

    assert pformat(FuncRegistered()) == "FUNC\n"


def test_register_func_runs_after_type_registration() -> None:
    @register_func
    def _describe_int_func(obj: object, _options: PrettyOptions) -> SpecLeaf | None:
        if not isinstance(obj, int):
            return None
        return SpecLeaf(cls=int, referable=False, text=Text("INT-FUNC"))

    assert pformat(1) == "1\n"


def test_missing_lazy_registration_logs_once_and_is_removed(
    caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    module_name = "tests.pretty_missing_lazy_module"
    module = types.ModuleType(module_name)
    monkeypatch.setitem(sys.modules, module_name, module)
    registry = DescribeRegistry()

    @registry.register_lazy(module_name, "Missing")
    def _describe_missing(_obj: object, _options: PrettyOptions) -> SpecLeaf:
        return SpecLeaf(cls=object, referable=False, text=Text("MISSING"))

    with caplog.at_level(logging.WARNING):
        assert registry(1, PrettyOptions()) is None
        assert registry(1, PrettyOptions()) is None

    assert registry.handlers_lazy == {}
    assert [record.message for record in caplog.records] == [
        f"failed to resolve lazy pretty handler for {module_name}.Missing"
    ]
