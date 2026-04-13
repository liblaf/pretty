from typing import Self, cast

import attrs


@attrs.frozen
class ObjectIdentifier:
    cls: type
    id_: int = attrs.field(alias="id")

    @classmethod
    def from_obj(cls, obj: object) -> Self:
        return cls(cls=type(obj), id=id(obj))

    @classmethod
    def missing(cls) -> Self:
        return cls(cls=cast("type", None), id=0)
