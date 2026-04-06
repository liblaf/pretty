from typing import Self

import attrs


@attrs.frozen
class TraceId:
    cls: type
    id_: int

    @classmethod
    def from_obj(cls, obj: object) -> Self:
        return cls(cls=type(obj), id_=id(obj))
