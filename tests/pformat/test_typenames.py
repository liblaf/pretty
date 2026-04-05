from collections.abc import Iterable

import attrs
from rich.text import Text

from liblaf.pretty import PrettyOptions, SpecContainer, SpecField, pformat


@attrs.frozen(slots=True, kw_only=True)
class SelfRefSpec(SpecContainer):
    owner: "SelfReferential"

    def iter_children(self) -> Iterable[SpecField]:
        yield SpecField(name="self", value=self.owner.spec)


class SelfReferential:
    spec: SelfRefSpec

    def __pretty__(self, _options: PrettyOptions) -> SelfRefSpec:
        return self.spec


def _make_self_ref_instance(cls: type[SelfReferential]) -> SelfReferential:
    obj = cls()
    obj.spec = SelfRefSpec(
        cls=type(obj),
        id_=id(obj),
        referable=True,
        begin=Text.assemble(
            (type(obj).__name__, "repr.tag_name"), ("(", "repr.tag_start")
        ),
        end=Text(")", "repr.tag_end"),
        owner=obj,
    )
    return obj


def test_module_suffix_disambiguation() -> None:
    left_cls = type("Thing", (SelfReferential,), {"__module__": "pkg.alpha"})
    right_cls = type("Thing", (SelfReferential,), {"__module__": "other.alpha"})
    left = _make_self_ref_instance(left_cls)
    right = _make_self_ref_instance(right_cls)

    text = pformat([left, right], options=PrettyOptions(max_width=200))
    assert "pkg.alpha.Thing object at" in text
    assert "other.alpha.Thing object at" in text


def test_qualname_suffix_disambiguation() -> None:
    class Outer1:
        class Thing(SelfReferential):
            pass

    class Outer2:
        class Thing(SelfReferential):
            pass

    left = _make_self_ref_instance(Outer1.Thing)
    right = _make_self_ref_instance(Outer2.Thing)

    text = pformat([left, right], options=PrettyOptions(max_width=200))
    assert "Outer1.Thing object at" in text
    assert "Outer2.Thing object at" in text
