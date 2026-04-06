import abc

import attrs

from liblaf.pretty._trace import Traced

from ._context import TraceContext


@attrs.define
class Spec[T: Traced](abc.ABC):
    @abc.abstractmethod
    def trace(self, ctx: TraceContext, depth: int) -> T: ...


"""
def trace() -> None:
    while queue:
        node, depth, parent, meta = queue.popleft()
        match node:
            case SpecLeaf:
                if node.ref in ctx.cache:
                    traced = TracedRef(node.ref)
                    ctx.cache[node.ref].ref = node.ref  # add annotation to the anchor
                else:
                    traced = TracedLeaf(node.value)  # do not add annotation now
                    ctx.cache[node.ref] = traced
            case SpecContainer:
                if node.ref in ctx.cache:
                    traced = TracedRef(node.ref)
                    ctx.cache[node.ref].ref = node.ref  # add annotation to the anchor
                else:
                    traced = TracedContainer(...)  # do not add annotation now
                    ctx.cache[node.ref] = traced
                    for item in node.items:
                        queue.append((item, depth + 1, traced))
            case SpecItemEntry:
                traced = TracedItemEntry(...)  # do not add annotation now
                queue.append((node.key, depth, traced))
                queue.append((node.value, depth, traced))
            case SpecItemField:
                traced = TracedItemField(...)  # do not add annotation now
                queue.append((node.value, depth, traced))
            case SpecItemValue:
                traced = TracedItemValue(...)  # do not add annotation now
                queue.append((node.value, depth, traced))
        match parent:
            case TracedContainer():
                parent.items.append(traced)
            case TracedItemEntry():
                if meta == "key":
                    parent.key = traced
                if meta == "value":
                    parent.value = traced
            case TracedItemField():
                assert parent.value is ...
                parent.value = traced
            case TracedItemValue():
                assert parent.value is ...
                parent.value = traced
"""
