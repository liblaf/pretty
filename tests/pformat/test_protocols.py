import dataclasses

from rich.repr import RichReprResult

from liblaf.pretty import PrettyBuilder, pformat


class SupportsPretty:
    def __liblaf_pretty__(self, builder: PrettyBuilder):
        return builder.leaf("SUPPORTS_PRETTY", referable=False)


def test_pretty_protocol() -> None:
    assert pformat(SupportsPretty()) == "SUPPORTS_PRETTY\n"


class MixedItems:
    def __liblaf_pretty__(self, builder: PrettyBuilder):
        return builder.object(
            [
                builder.value("leaf0"),
                builder.value("leaf1"),
                builder.entry("key1", "value1"),
                builder.field("name2", "value2"),
            ],
            referable=False,
        )


def test_mixed_items() -> None:
    assert (
        pformat(MixedItems())
        == "MixedItems('leaf0', 'leaf1', 'key1': 'value1', name2='value2')\n"
    )


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
