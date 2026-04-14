"""Object identifiers used for shared-reference tracking."""

from typing import Self

import attrs


@attrs.frozen
class ObjectIdentifier:
    """Stable identifier for a potentially referencable object."""

    cls: type | None
    id_: int | None = attrs.field(alias="id")

    @classmethod
    def from_obj(cls, obj: object) -> Self:
        """Create an identifier from a live object."""
        return cls(cls=type(obj), id=id(obj))

    @classmethod
    def missing(cls) -> Self:
        """Return an identifier for nodes without a backing object."""
        return cls(cls=None, id=None)
