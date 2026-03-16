from liblaf.pretty import pformat


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
