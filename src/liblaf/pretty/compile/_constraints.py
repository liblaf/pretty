from __future__ import annotations

from typing import ClassVar, Self, TypedDict, Unpack

import attrs


@attrs.frozen(kw_only=True)
class Flags:
    multiline: bool
    break_before: bool = False
    break_after: bool = False


@attrs.frozen(kw_only=True)
class Constraints:
    BLOCK: ClassVar[Constraints]
    INLINE: ClassVar[Constraints]
    KEY: ClassVar[Constraints]
    VALUE: ClassVar[Constraints]

    allow_multiline: bool = True
    allow_break_before: bool = True
    allow_break_after: bool = True

    def allow(self, flags: Flags) -> bool:
        return (
            (self.allow_multiline or not flags.multiline)
            and (self.allow_break_before or not flags.break_before)
            and (self.allow_break_after or not flags.break_after)
        )

    class _Override(TypedDict, total=False):
        allow_multiline: bool
        allow_break_before: bool
        allow_break_after: bool

    def override(self, **kwargs: Unpack[_Override]) -> Self:
        return attrs.evolve(self, **kwargs)


Constraints.BLOCK = Constraints()
Constraints.INLINE = Constraints(
    allow_multiline=False, allow_break_before=False, allow_break_after=False
)
Constraints.KEY = Constraints(allow_break_after=False)
Constraints.VALUE = Constraints(allow_break_before=False)
