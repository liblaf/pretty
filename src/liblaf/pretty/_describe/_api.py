from __future__ import annotations

import reprlib
import types
from collections.abc import Iterable, Mapping
from typing import Any, cast

import attrs
from rich.highlighter import ReprHighlighter
from rich.text import Text

from liblaf.pretty._options import PrettyOptions
from liblaf.pretty._spec import (
    Spec,
    SpecContainer,
    SpecItem,
    SpecKeyValue,
    SpecLeaf,
    SpecValue,
)
from liblaf.pretty._utils._text import has_ansi

from ._registry import describe_registry, register_type

_HIGHLIGHTER = ReprHighlighter()
_TRUE = Text("True", "repr.bool_true")
_FALSE = Text("False", "repr.bool_false")
_NONE = Text("None", "repr.none")
_ELLIPSIS = Text("...", "repr.ellipsis")


def _make_repr(options: PrettyOptions) -> reprlib.Repr:
    return reprlib.Repr(
        maxlevel=options.max_level,
        maxtuple=options.max_list,
        maxlist=options.max_list,
        maxdict=options.max_dict,
        maxset=options.max_list,
        maxfrozenset=options.max_list,
        maxdeque=options.max_list,
        maxstring=options.max_string,
        maxlong=options.max_long,
        maxother=options.max_other,
        indent=options.indent.plain,
    )


def _repr_text(obj: object, options: PrettyOptions) -> Text:
    text: str = _make_repr(options).repr(obj)
    if has_ansi(text):
        return Text.from_ansi(text)
    return _HIGHLIGHTER(text)


@attrs.frozen(slots=True, kw_only=True)
class _SequenceSpec(SpecContainer):
    items: tuple[Any, ...]
    options: PrettyOptions

    def iter_children(self) -> Iterable[SpecItem]:
        for value in self.items:
            yield SpecValue(value=describe(value, self.options))


@attrs.frozen(slots=True, kw_only=True)
class _TupleSpec(_SequenceSpec):
    def force_comma_if_single(self) -> bool:
        return True


@attrs.frozen(slots=True, kw_only=True)
class _MappingSpec(SpecContainer):
    items: tuple[tuple[Any, Any], ...]
    options: PrettyOptions

    def iter_children(self) -> Iterable[SpecItem]:
        for key, value in self.items:
            yield SpecKeyValue(
                key=describe(key, self.options),
                value=describe(value, self.options),
            )

    def max_items(self, options: PrettyOptions) -> int:
        return options.max_dict


@register_type(bool)
def _describe_bool(obj: object, _options: PrettyOptions) -> SpecLeaf:
    value = cast("bool", obj)
    return SpecLeaf(
        cls=bool,
        referable=False,
        text=_TRUE if value else _FALSE,
    )


@register_type(types.NoneType)
def _describe_none(_value: None, _options: PrettyOptions) -> SpecLeaf:
    return SpecLeaf(cls=types.NoneType, referable=False, text=_NONE)


@register_type(types.EllipsisType)
def _describe_ellipsis(_value: types.EllipsisType, _options: PrettyOptions) -> SpecLeaf:
    return SpecLeaf(
        cls=types.EllipsisType,
        referable=False,
        text=_ELLIPSIS,
    )


@register_type(int)
@register_type(float)
@register_type(complex)
@register_type(range)
@register_type(str)
@register_type(bytes)
@register_type(bytearray)
@register_type(memoryview)
@register_type(type)
def _describe_scalar(obj: object, options: PrettyOptions) -> SpecLeaf:
    return SpecLeaf(
        cls=type(obj),
        referable=False,
        text=_repr_text(obj, options),
    )


@register_type(list)
def _describe_list(obj: list[object], options: PrettyOptions) -> SpecContainer:
    return _SequenceSpec(
        cls=type(obj),
        id_=id(obj),
        referable=True,
        begin=Text("[", "repr.tag_start"),
        end=Text("]", "repr.tag_end"),
        items=tuple(obj),
        options=options,
    )


@register_type(tuple)
def _describe_tuple(obj: tuple[object, ...], options: PrettyOptions) -> SpecContainer:
    return _TupleSpec(
        cls=type(obj),
        id_=id(obj),
        referable=True,
        begin=Text("(", "repr.tag_start"),
        end=Text(")", "repr.tag_end"),
        items=tuple(obj),
        options=options,
    )


@register_type(set)
def _describe_set(obj: set[object], options: PrettyOptions) -> SpecContainer:
    return _SequenceSpec(
        cls=type(obj),
        id_=id(obj),
        referable=True,
        begin=Text("{", "repr.tag_start"),
        end=Text("}", "repr.tag_end"),
        empty=Text.assemble(
            ("set", "repr.tag_name"),
            ("(", "repr.tag_start"),
            (")", "repr.tag_end"),
        ),
        items=tuple(obj),
        options=options,
    )


@register_type(frozenset)
def _describe_frozenset(
    obj: frozenset[object], options: PrettyOptions
) -> SpecContainer:
    return _SequenceSpec(
        cls=type(obj),
        id_=id(obj),
        referable=True,
        begin=Text.assemble(
            ("frozenset", "repr.tag_name"),
            ("({", "repr.tag_start"),
        ),
        end=Text("})", "repr.tag_end"),
        empty=Text.assemble(
            ("frozenset", "repr.tag_name"),
            ("(", "repr.tag_start"),
            (")", "repr.tag_end"),
        ),
        items=tuple(obj),
        options=options,
    )


@register_type(dict)
def _describe_dict(
    obj: Mapping[object, object], options: PrettyOptions
) -> SpecContainer:
    return _MappingSpec(
        cls=type(obj),
        id_=id(obj),
        referable=True,
        begin=Text("{", "repr.tag_start"),
        end=Text("}", "repr.tag_end"),
        items=tuple(cast("Mapping[Any, Any]", obj).items()),
        options=options,
    )


def _describe_fallback(obj: object, options: PrettyOptions) -> SpecLeaf:
    return SpecLeaf(
        cls=type(obj),
        id_=id(obj),
        referable=True,
        text=_repr_text(obj, options),
    )


def describe(obj: object, options: PrettyOptions) -> Spec:
    pretty = getattr(obj, "__pretty__", None)
    if pretty is not None:
        spec: object = pretty(options)
        if not isinstance(spec, Spec):
            msg = "__pretty__() must return a Spec"
            raise TypeError(msg)
        return spec
    spec = describe_registry(obj, options)
    if spec is not None:
        return spec
    return _describe_fallback(obj, options)
