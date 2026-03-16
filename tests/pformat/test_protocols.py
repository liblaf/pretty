import dataclasses
from typing import Any

from rich.repr import RichReprResult
from rich.text import Text

from liblaf.pretty import TracedLeaf, pformat


class SupportsPretty:
    def __liblaf_pretty__(self, _ctx: Any) -> TracedLeaf:
        return TracedLeaf(Text("SUPPORTS_PRETTY"))


def test_pretty_protocol() -> None:
    assert pformat(SupportsPretty()) == "SUPPORTS_PRETTY\n"


class SupportsRichRepr:
    def __rich_repr__(self) -> RichReprResult:
        yield "foo"
        yield "bar", "bar"
        yield "baz", None, None


def test_rich_repr() -> None:
    obj: SupportsRichRepr = SupportsRichRepr()
    assert pformat(obj) == "SupportsRichRepr('foo', bar='bar')\n"
    assert (
        pformat(obj, hide_defaults=False)
        == "SupportsRichRepr('foo', bar='bar', baz=None)\n"
    )


@dataclasses.dataclass
class Dataclass:
    foo: str = dataclasses.field()
    _hidden: str = dataclasses.field(repr=False)
    bar: str = dataclasses.field(default="bar")


def test_dataclass() -> None:
    obj: Dataclass = Dataclass(foo="foo", _hidden="hidden")
    assert pformat(obj) == "Dataclass(foo='foo')\n"
    assert pformat(obj, hide_defaults=False) == "Dataclass(foo='foo', bar='bar')\n"
