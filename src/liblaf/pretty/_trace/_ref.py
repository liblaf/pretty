from typing import Self

import attrs


@attrs.frozen
class Ref:
    cls: type
    id_: int

    @classmethod
    def from_obj(cls, obj: object) -> Self:
        return cls(cls=type(obj), id_=id(obj))
