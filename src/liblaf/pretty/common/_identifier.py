
from typing import Self

import attrs


@attrs.frozen
class ObjectIdentifier:

    cls: type | None
    id_: int | None = attrs.field(alias="id")

    @classmethod
    def from_obj(cls, obj: object) -> Self:
        return cls(cls=type(obj), id=id(obj))

    @classmethod
    def missing(cls) -> Self:
        return cls(cls=None, id=None)
