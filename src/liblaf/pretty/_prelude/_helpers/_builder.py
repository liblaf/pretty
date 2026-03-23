from collections.abc import Iterable
from typing import Protocol, runtime_checkable

import attrs
from rich.highlighter import Highlighter, ReprHighlighter
from rich.text import Text

from liblaf.pretty._api._config import PrettyOptions
from liblaf.pretty._api._text import has_ansi

from ._common import PrettyChild, copy_text
from ._items import EntryItemSpec, FieldItemSpec, ItemSpec, ValueItemSpec
from ._specs import ContainerSpec, LeafSpec, LiteralSpec, PrettySpec


@runtime_checkable
class SupportsPretty(Protocol):
    def __liblaf_pretty__(self, builder: "PrettyBuilder") -> PrettySpec | None: ...


@attrs.define
class PrettyBuilder:
    options: PrettyOptions
    _highlighter: Highlighter | None = attrs.field(
        factory=ReprHighlighter, kw_only=True
    )

    def text(self, text: str | Text) -> LiteralSpec:
        return LiteralSpec(copy_text(text))

    def ellipsis(self) -> LiteralSpec:
        return LiteralSpec(Text("...", "repr.ellipsis"))

    def leaf(self, text: str | Text, *, referable: bool = True) -> LeafSpec:
        return LeafSpec(copy_text(text), referable=referable)

    def container(
        self,
        items: Iterable[ItemSpec],
        *,
        open_brace: str,
        close_brace: str,
        empty_open: str | None = None,
        empty_close: str | None = None,
        show_type_name: bool = False,
        trailing_comma_single: bool = False,
        referable: bool = True,
    ) -> ContainerSpec:
        return ContainerSpec(
            items=tuple(items),
            open_brace=open_brace,
            close_brace=close_brace,
            empty_open_brace=empty_open if empty_open is not None else open_brace[:1],
            empty_close_brace=(
                empty_close if empty_close is not None else close_brace[-1:]
            ),
            show_type_name=show_type_name,
            trailing_comma_single=trailing_comma_single,
            referable=referable,
        )

    def object(
        self,
        items: Iterable[ItemSpec],
        *,
        open_brace: str = "(",
        close_brace: str = ")",
        referable: bool = True,
    ) -> ContainerSpec:
        return self.container(
            items,
            open_brace=open_brace,
            close_brace=close_brace,
            show_type_name=True,
            referable=referable,
        )

    def value(self, child: PrettyChild) -> ValueItemSpec:
        return ValueItemSpec(child)

    def entry(self, key: PrettyChild, value: PrettyChild) -> EntryItemSpec:
        return EntryItemSpec(key=key, value=value)

    def field(self, name: str, value: PrettyChild) -> FieldItemSpec:
        return FieldItemSpec(name=name, value=value)

    def highlight(self, text: str) -> Text:
        if has_ansi(text):
            return Text.from_ansi(text)
        if self._highlighter is None:
            return Text(text)
        return self._highlighter(text)
