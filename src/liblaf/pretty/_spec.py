from __future__ import annotations

import abc
from collections.abc import Iterable
from typing import TYPE_CHECKING, Protocol

import attrs
from rich.text import Text

if TYPE_CHECKING:
    from ._options import PrettyOptions


def _to_text(value: Text | str) -> Text:
    if isinstance(value, Text):
        return value.copy()
    return Text(str(value))


def _to_optional_text(value: Text | str | None) -> Text | None:
    if value is None:
        return None
    return _to_text(value)


@attrs.frozen(slots=True, hash=False)
class Spec:
    cls: type
    id_: int | None = None
    referable: bool = True


@attrs.frozen(slots=True, kw_only=True, hash=False)
class SpecLeaf(Spec):
    text: Text = attrs.field(converter=_to_text)


@attrs.frozen(slots=True, hash=False)
class SpecItem:
    pass


@attrs.frozen(slots=True, hash=False)
class SpecValue(SpecItem):
    value: Spec


@attrs.frozen(slots=True, hash=False)
class SpecField(SpecItem):
    name: str
    value: Spec


@attrs.frozen(slots=True, hash=False)
class SpecKeyValue(SpecItem):
    key: Spec
    value: Spec


@attrs.frozen(slots=True, kw_only=True, hash=False)
class SpecContainer(Spec, abc.ABC):
    begin: Text = attrs.field(converter=_to_text)
    end: Text = attrs.field(converter=_to_text)
    empty: Text | None = attrs.field(default=None, converter=_to_optional_text)

    @abc.abstractmethod
    def iter_children(self) -> Iterable[SpecItem]:
        raise NotImplementedError

    def empty_text(self) -> Text:
        if self.empty is not None:
            return self.empty.copy()
        return Text.assemble(self.begin, self.end)

    def force_comma_if_single(self) -> bool:
        return False

    def max_items(self, options: PrettyOptions) -> int:
        return options.max_list


class PrettyPrintable(Protocol):
    def __pretty__(self, options: PrettyOptions) -> Spec: ...
