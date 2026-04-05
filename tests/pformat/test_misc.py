from rich.text import Text

from liblaf.pretty import PrettyOptions, SpecLeaf, pformat


def test_scalars() -> None:
    assert pformat(True) == "True\n"  # noqa: FBT003
    assert pformat(False) == "False\n"  # noqa: FBT003
    assert pformat(None) == "None\n"
    assert pformat(...) == "...\n"


def test_repr() -> None:
    class Repr:
        def __repr__(self) -> str:
            return "REPR"

    assert pformat(Repr()) == "REPR\n"


def test_text_inputs_are_copied() -> None:
    indent = Text("-> ")
    options = PrettyOptions(indent=indent)
    indent.append("mutated")
    assert options.indent.plain == "-> "

    text = Text("leaf")
    spec = SpecLeaf(cls=str, referable=False, text=text)
    text.append(" mutated")
    assert spec.text.plain == "leaf"
