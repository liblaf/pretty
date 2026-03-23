from collections.abc import Generator
from typing import Any

import fieldz

from .. import ContainerSpec, PrettyBuilder

from ..._trace._registry import registry
from ._helpers import filter_fields


@registry.register_fallback
def _trace_fieldz(obj: Any, builder: PrettyBuilder) -> ContainerSpec | None:
    try:
        fields: tuple[fieldz.Field, ...] = fieldz.fields(obj, parse_annotated=False)
    except TypeError:
        return None

    def field_generator() -> Generator[tuple[str | None, Any]]:
        for field in fields:
            if not field.repr:
                continue
            value: Any = getattr(obj, field.name, fieldz.Field.MISSING)
            if builder.options.hide_defaults and value is field.default:
                continue
            yield field.name, value

    return builder.object(filter_fields(builder, field_generator()), referable=True)
