
import attrs


@attrs.frozen
class LowerContext:

    typenames: dict[type, str]

    def get_ref_typename(self, cls: type) -> str:
        return self.typenames.get(cls) or cls.__name__

    def get_tag_typename(self, cls: type) -> str:
        return self.typenames.get(cls, cls.__name__)
