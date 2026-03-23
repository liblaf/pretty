from liblaf.pretty._prelude import ContainerSpec, PrettyBuilder

from .._registry import registry
from ._helpers import truncate_mapping, truncate_sequence


@registry.register(list)
def _trace_list(obj: list, builder: PrettyBuilder) -> ContainerSpec:
    return builder.container(
        truncate_sequence(builder, obj, builder.options.max_list),
        open="[",
        close="]",
        referable=True,
    )


@registry.register(tuple)
def _trace_tuple(obj: tuple, builder: PrettyBuilder) -> ContainerSpec:
    return builder.container(
        truncate_sequence(builder, obj, builder.options.max_list),
        open="(",
        close=")",
        trailing_comma_single=True,
        referable=True,
    )


@registry.register(set)
def _trace_set(obj: set, builder: PrettyBuilder) -> ContainerSpec:
    return builder.container(
        truncate_sequence(builder, obj, builder.options.max_list),
        open="{",
        close="}",
        referable=True,
    )


@registry.register(frozenset)
def _trace_frozenset(obj: frozenset, builder: PrettyBuilder) -> ContainerSpec:
    return builder.container(
        truncate_sequence(builder, obj, builder.options.max_list),
        open="({",
        close="})",
        empty_open="(",
        empty_close=")",
        show_type_name=True,
        referable=True,
    )


@registry.register(dict)
def _trace_dict(obj: dict, builder: PrettyBuilder) -> ContainerSpec:
    return builder.container(
        truncate_mapping(builder, obj.items(), builder.options.max_dict),
        open="{",
        close="}",
        referable=True,
    )
