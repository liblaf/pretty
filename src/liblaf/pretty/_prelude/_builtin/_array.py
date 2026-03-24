from __future__ import annotations

import re
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from rich.text import Text

from liblaf.pretty._compile import COMMA
from liblaf.pretty._trace._helpers._builder import PrettyBuilder
from liblaf.pretty._trace._helpers._specs import LeafSpec
from liblaf.pretty._trace._registry import registry

if TYPE_CHECKING:
    import jax
    import numpy as np
    import torch
    import warp as wp


@registry.register_lazy("jax", "Array")
def _trace_jax_array(obj: jax.Array, builder: PrettyBuilder) -> LeafSpec | None:
    if all(dim <= builder.options.max_array for dim in obj.shape):
        import jax.numpy as jnp

        with jnp.printoptions(
            threshold=builder.options.max_array ** len(obj.shape),
            edgeitems=builder.options.max_array // 2,
        ):
            return LeafSpec(builder.highlight(_indent_repr(repr(obj), "jax.")))
    return _short_array(_short_dtype(obj.dtype), obj.shape, "jax")


@registry.register_lazy("numpy", "ndarray")
def _trace_ndarray(obj: np.ndarray, builder: PrettyBuilder) -> LeafSpec | None:
    import numpy as np

    if all(dim <= builder.options.max_array for dim in obj.shape):
        with np.printoptions(
            threshold=builder.options.max_array ** len(obj.shape),
            edgeitems=builder.options.max_array // 2,
        ):
            return LeafSpec(builder.highlight(_indent_repr(repr(obj), "numpy.")))
    return _short_array(_short_dtype(obj.dtype), obj.shape, "numpy")


@registry.register_lazy("torch", "Tensor")
def _trace_tensor(obj: torch.Tensor, builder: PrettyBuilder) -> LeafSpec | None:
    from torch._tensor_str import printoptions

    if all(dim <= builder.options.max_array for dim in obj.shape):
        with printoptions(
            threshold=builder.options.max_array ** len(obj.shape),
            edgeitems=builder.options.max_array // 2,
        ):
            return LeafSpec(builder.highlight(_indent_repr(repr(obj), "torch.")))
    return _short_array(_short_dtype(obj.dtype), obj.shape, "torch")


@registry.register_lazy("warp", "array")
def _trace_warp_array(obj: wp.array, builder: PrettyBuilder) -> LeafSpec | None:
    import warp as wp

    dtype: str = wp.types.type_repr(obj.dtype)
    if len(dtype) > 8:
        return LeafSpec(
            builder.highlight(
                "warp."
                + wp.types.type_repr(obj)
                .replace("dtype=", "")
                .replace("length=", "")
                .replace("shape=", "")
            )
        )
    dtype: str = _short_dtype(dtype, strip_module=False)
    dtype: str = re.sub(r"\((?P<scalar>[a-zA-Z])\)", r"\g<scalar>", dtype)
    return _short_array(dtype, obj.shape, "warp")


def _indent_repr(text: str, prefix: str) -> str:
    segments: list[str] = []
    subsequent_prefix: str = " " * len(prefix)
    for i, line in enumerate(text.splitlines(keepends=True)):
        segments.append(prefix if i == 0 else subsequent_prefix)
        segments.append(line)
    return "".join(segments)


def _short_array(dtype: str, shape: Iterable[int], module: str) -> LeafSpec:
    return LeafSpec(
        Text.assemble(
            dtype,
            "[",
            COMMA.join(Text(str(dim), "repr.number") for dim in shape),
            "]",
            f"({module})",
        )
    )


def _short_shape(shape: Iterable[int]) -> str:
    return ",".join(map(str, shape))


def _short_dtype(dtype: Any, *, strip_module: bool = True) -> str:
    if strip_module:
        _, _, dtype = str(dtype).rpartition(".")
    dtype = (
        dtype.replace("bool", "?")
        .replace("uint", "u")
        .replace("int", "i")
        .replace("float", "f")
        .replace("complex", "c")
    )
    return dtype
