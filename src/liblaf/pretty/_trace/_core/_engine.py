from __future__ import annotations

from collections import deque

import attrs

from liblaf.pretty._api._config import PrettyOptions
from liblaf.pretty._prelude._helpers._builder import PrettyBuilder
from liblaf.pretty._trace._registry import PrettyRegistry, registry

from ._describe import describe, make_node
from ._expand import expand_occurrence, truncate_container
from ._nodes import TracedContainerNode, TracedNode
from ._occurrence import TracedOccurrence, TraceResult


@attrs.define
class TraceEngine:
    options: PrettyOptions
    registry: PrettyRegistry = attrs.field(default=registry, kw_only=True)
    builder: PrettyBuilder = attrs.field(init=False)
    _nodes_by_id: dict[int, TracedNode] = attrs.field(factory=dict, init=False)
    _tracked_types: set[type] = attrs.field(factory=set, init=False)
    _queue: deque[TracedOccurrence] = attrs.field(factory=deque, init=False)

    def __attrs_post_init__(self) -> None:
        self.builder = PrettyBuilder(self.options)

    def trace(self, root: object) -> TraceResult:
        self._nodes_by_id.clear()
        self._tracked_types.clear()
        self._queue.clear()
        root_occurrence: TracedOccurrence = self._discover(root, 0, (), ())
        while self._queue:
            expand_occurrence(
                self._queue.popleft(),
                discover=self._discover,
            )
        return TraceResult(
            root=root_occurrence,
            nodes_by_id=dict(self._nodes_by_id),
            tracked_types=set(self._tracked_types),
        )

    def _discover(
        self,
        obj: object,
        depth: int,
        path: tuple[int, ...],
        ancestors: tuple[int, ...],
    ) -> TracedOccurrence:
        obj_id: int = id(obj)
        node: TracedNode | None = self._nodes_by_id.get(obj_id)
        if node is not None:
            node.appearance_count += 1
            kind: str = "cycle" if obj_id in ancestors else "repeat"
            return TracedOccurrence(node, kind, path, depth, ancestors=ancestors)
        spec = describe(obj, builder=self.builder, registry=self.registry)
        node = make_node(obj, spec)
        self._nodes_by_id[obj_id] = node
        self._tracked_types.add(type(obj))
        occurrence = TracedOccurrence(node, "anchor", path, depth, ancestors=ancestors)
        if isinstance(node, TracedContainerNode):
            if depth >= self.options.max_level:
                node.items = truncate_container(node, builder=self.builder)
                node.expanded = True
            else:
                self._queue.append(occurrence)
        return occurrence


def trace(
    obj: object, *, options: PrettyOptions, registry: PrettyRegistry = registry
) -> TraceResult:
    return TraceEngine(options=options, registry=registry).trace(obj)
