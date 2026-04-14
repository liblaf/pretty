"""Context used while lowering traced nodes."""

import attrs


@attrs.frozen
class LowerContext:
    """Resolved type-name mapping used when lowering traced nodes."""

    typenames: dict[type, str]

    def get_ref_typename(self, cls: type) -> str:
        """Return the name used inside `<Type @ hexid>` references."""
        return self.typenames.get(cls) or cls.__name__

    def get_tag_typename(self, cls: type) -> str:
        """Return the name used at the start of tagged containers."""
        return self.typenames.get(cls, cls.__name__)
