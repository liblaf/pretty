from __future__ import annotations

from liblaf.pretty._options import PrettyOptions
from liblaf.pretty._spec import Spec

from ._bfs import build_traced
from ._model import TracedDocument


def trace(spec: Spec, options: PrettyOptions) -> TracedDocument:
    return build_traced(spec, options)
