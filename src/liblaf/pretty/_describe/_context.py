import contextlib
from collections.abc import Generator
from typing import Any, Self

import attrs
from rich.text import Text

from liblaf.pretty._conf import PrettyOptions, config
from liblaf.pretty._spec import Spec, SpecLeaf


@attrs.define
class DescribeContext:
    options: PrettyOptions = attrs.field(factory=config.dump)
    specs: dict[int, Spec] = attrs.field(factory=dict)

    def describe(self, obj: Any) -> Spec:
        id_: int = id(obj)
        if id_ in self.specs:
            return self.specs[id_]
        spec: Spec = SpecLeaf(
            cls=type(obj), id_=id_, value=Text(repr(obj)), referenceable=False
        )
        self.specs[id_] = spec
        return spec

    @contextlib.contextmanager
    def nest(self) -> Generator[Self]:
        old_depth: int = self.depth
        self.depth += 1
        try:
            yield self
        finally:
            self.depth = old_depth
