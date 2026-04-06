from collections import Counter

import attrs

from liblaf.pretty._conf import PrettyOptions, config
from liblaf.pretty._trace import TracedObject


@attrs.define
class TraceContext:
    depth: int = 0
    cache: dict[int, TracedObject] = attrs.field(factory=dict)
    id_counter: Counter[int] = attrs.field(factory=Counter)
    options: PrettyOptions = attrs.field(factory=config.dump)
