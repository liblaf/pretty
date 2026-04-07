from ._context import DescribeContext
from ._lazy import LazySpec
from ._registry import DescribeRegistry, describe
from ._repr import describe_repr

__all__ = [
    "DescribeContext",
    "DescribeRegistry",
    "LazySpec",
    "describe",
    "describe_repr",
]
