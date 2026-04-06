from collections import Counter
from collections.abc import Generator
from typing import Self

import attrs

from liblaf.pretty._conf import PrettyOptions, config


@attrs.define
class TraceContext:
    depth: int = 0
    id_counter: Counter[int] = attrs.field(factory=Counter)
    options: PrettyOptions = attrs.field(factory=config.dump)

    def nest(self) -> Generator[Self]:
        self.depth += 1
        try:
            yield self
        finally:
            self.depth -= 1
