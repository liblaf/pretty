from collections.abc import Callable
from typing import Any, overload

from ._describe._registry import DescribeFunc, DescribeTypeHandler
from ._main import pdoc, pformat, pprint
from ._options import PrettyOptions
from ._spec import (
    PrettyPrintable,
    Spec,
    SpecContainer,
    SpecField,
    SpecItem,
    SpecKeyValue,
    SpecLeaf,
    SpecValue,
)

@overload
def register_type[F: DescribeTypeHandler[Any]](cls: type, handler: F) -> F: ...
@overload
def register_type[F: DescribeTypeHandler[Any]](
    cls: type, handler: None = None
) -> Callable[[F], F]: ...
@overload
def register_lazy[F: DescribeTypeHandler[Any]](
    module: str, typename: str, handler: F
) -> F: ...
@overload
def register_lazy[F: DescribeTypeHandler[Any]](
    module: str, typename: str, handler: None = None
) -> Callable[[F], F]: ...
def register_func[F: DescribeFunc](handler: F) -> F: ...

__all__ = [
    "PrettyOptions",
    "PrettyPrintable",
    "Spec",
    "SpecContainer",
    "SpecField",
    "SpecItem",
    "SpecKeyValue",
    "SpecLeaf",
    "SpecValue",
    "pdoc",
    "pformat",
    "pprint",
    "register_func",
    "register_lazy",
    "register_type",
]
