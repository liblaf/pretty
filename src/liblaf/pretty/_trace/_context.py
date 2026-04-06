import attrs
from rich.text import Text


@attrs.frozen
class LowerContext:
    typenames: dict[type, str]

    def make_anchor(self, cls: type, id_: int) -> Text:
        typename: str = self.get_ref_typename(cls)
        return Text(f"  # <{typename} @ {id_:x}>", "dim")

    def make_ref(self, cls: type, id_: int) -> Text:
        typename: str = self.get_ref_typename(cls)
        return Text.assemble(
            ("<", "repr.tag_start"),
            (typename, "repr.tag_name"),
            (f" @ {id_:x}", "repr.tag_contents"),
            (">", "repr.tag_end"),
        )

    def get_container_typename(self, cls: type) -> str:
        return self.typenames.get(cls, cls.__name__)

    def get_ref_typename(self, cls: type) -> str:
        return self.typenames.get(cls) or cls.__name__
