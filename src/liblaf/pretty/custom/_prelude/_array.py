"""Lazy summaries for optional array and tensor libraries."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from rich.text import Text

from liblaf.pretty.custom._context import PrettyContext
from liblaf.pretty.custom._registry import registry
from liblaf.pretty.stages.wrapped import WrappedNode

if TYPE_CHECKING:
    import jax
    import numpy as np
    import torch
    import warp as wp


@registry.register_lazy("jax", "Array")
def _pretty_jax_array(obj: jax.Array, ctx: PrettyContext) -> WrappedNode | None:
    return _array_summary(obj, ctx, str(obj.dtype), obj.shape, "jax")


@registry.register_lazy("numpy", "ndarray")
def _pretty_numpy_array(obj: np.ndarray, ctx: PrettyContext) -> WrappedNode | None:
    return _array_summary(obj, ctx, str(obj.dtype), obj.shape, "numpy")


@registry.register_lazy("torch", "Tensor")
def _pretty_torch_tensor(obj: torch.Tensor, ctx: PrettyContext) -> WrappedNode | None:
    return _array_summary(obj, ctx, str(obj.dtype), obj.shape, "torch")


@registry.register_lazy("warp", "array")
def _pretty_warp_array(obj: wp.array, ctx: PrettyContext) -> WrappedNode | None:
    return _array_summary(obj, ctx, str(obj.dtype), obj.shape, "warp")


def _array_summary(
    obj: Any, ctx: PrettyContext, dtype: str, shape: Sequence[int], module: str
) -> WrappedNode | None:
    """Return a compact dtype-and-shape summary when the array is small enough.

    Any dimension larger than `max_array` declines the handler so the normal repr
    fallback can describe the value instead.
    """
    for d in shape:
        if d > ctx.options.max_array:
            return None
    dtype: str = (
        dtype.replace("float", "f")
        .replace("uint", "u")
        .replace("int", "i")
        .replace("complex", "c")
    )
    return ctx.leaf(
        obj,
        Text.assemble(
            dtype,
            ("[", "repr.brace"),
            Text(",", "repr.comma").join(Text(str(d), "repr.number") for d in shape),
            ("]", "repr.brace"),
            "(",
            module,
            ")",
        ),
    )
