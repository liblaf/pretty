from liblaf.pretty import pformat


def test_jax_small() -> None:
    import jax.numpy as jnp

    assert (
        pformat(jnp.zeros((2, 3)))
        == """\
jax.Array([[0., 0., 0.],
           [0., 0., 0.]], dtype=float32)
"""
    )


def test_jax_large() -> None:
    import jax.numpy as jnp

    assert pformat(jnp.zeros((20, 30))) == "f32[20,30](jax)\n"


def test_numpy_small() -> None:
    import numpy as np

    assert (
        pformat(np.zeros((2, 3)))
        == """\
numpy.array([[0., 0., 0.],
             [0., 0., 0.]])
"""
    )


def test_numpy_large() -> None:
    import numpy as np

    assert pformat(np.zeros((20, 30))) == "f64[20,30](numpy)\n"


def test_torch_small() -> None:
    import torch

    assert (
        pformat(torch.zeros((2, 3)))
        == """\
torch.tensor([[0., 0., 0.],
              [0., 0., 0.]])
"""
    )


def test_torch_large() -> None:
    import torch

    assert pformat(torch.zeros((20, 30))) == "f32[20,30](torch)\n"


def test_warp_scalar() -> None:
    import warp as wp

    assert pformat(wp.zeros((2, 3), dtype=wp.float32)) == "f32[2,3](warp)\n"


def test_warp_small_vector() -> None:
    import warp as wp

    assert pformat(wp.zeros((2, 3), dtype=wp.vec3f)) == "vec3f[2,3](warp)\n"


def test_warp_small_matrix() -> None:
    import warp as wp

    assert pformat(wp.zeros((2, 3), dtype=wp.mat33f)) == "mat33f[2,3](warp)\n"


def test_warp_large_vector() -> None:
    import warp as wp

    assert (
        pformat(wp.zeros((2, 3), dtype=wp.types.vector(5, wp.float32)))
        == "warp.array((2, 3), vector(5, float32))\n"
    )


def test_warp_large_matrix() -> None:
    import warp as wp

    assert (
        pformat(wp.zeros((2, 3), dtype=wp.types.matrix((5, 5), wp.float32)))
        == "warp.array((2, 3), matrix((5, 5), float32))\n"
    )
