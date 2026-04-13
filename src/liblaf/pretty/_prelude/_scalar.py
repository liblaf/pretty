import types
from typing import Any

from rich.text import Text

from liblaf.pretty._describe import DescribeContext, describe, describe_repr
from liblaf.pretty._spec import SpecLeaf, SpecNode
from liblaf.pretty._trace import ObjectIdentifier


@describe.register_type(types.NoneType)
def _describe_none(obj: None, _ctx: DescribeContext, _depth: int) -> SpecNode:
    return SpecLeaf(
        Text("None", "repr.none"),
        ref=ObjectIdentifier.from_obj(obj),
        referencable=False,
    )


@describe.register_type(types.EllipsisType)
def _describe_ellipsis(
    obj: types.EllipsisType, _ctx: DescribeContext, _depth: int
) -> SpecNode:
    return SpecLeaf(
        Text("...", "repr.ellipsis"),
        ref=ObjectIdentifier.from_obj(obj),
        referencable=False,
    )


@describe.register_type(bool)
def _describe_bool(obj: bool, _ctx: DescribeContext, _depth: int) -> SpecNode:  # noqa: FBT001
    text: Text = (
        Text("True", "repr.bool_true") if obj else Text("False", "repr.bool_false")
    )
    return SpecLeaf(
        text,
        ref=ObjectIdentifier.from_obj(obj),
        referencable=False,
    )


@describe.register_type(bytearray)
@describe.register_type(bytes)
@describe.register_type(complex)
@describe.register_type(float)
@describe.register_type(int)
@describe.register_type(memoryview)
@describe.register_type(str)
def _describe_scalar(obj: Any, ctx: DescribeContext, depth: int) -> SpecNode:
    return describe_repr(obj, ctx, depth, referencable=False)
