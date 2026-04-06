from typing import Any

import attrs
from rich.text import Text

from liblaf.pretty._conf import PrettyOptions, config
from liblaf.pretty._spec import SpecLeaf, SpecObject, TraceContext
from liblaf.pretty._trace import TraceId


@attrs.define
class DescribeContext:
    options: PrettyOptions = attrs.field(factory=config.dump)

    def describe(self, obj: Any) -> SpecObject:
        if isinstance(obj, list):
            from ._builtin_container import _describe_list

            return _describe_list(obj, self)
        # TODO: handle various types of objects
        return SpecLeaf(
            value=Text(repr(obj)), ref=TraceId.from_obj(obj), referencable=False
        )

    def finish(self) -> TraceContext:
        ctx: TraceContext = TraceContext(options=self.options)
        return ctx
