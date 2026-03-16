import contextlib
import functools
import reprlib
import types
from collections import Counter
from collections.abc import Mapping
from typing import Self, Unpack

import attrs
from rich.highlighter import Highlighter, ReprHighlighter
from rich.text import Text

from liblaf.pretty import _utils
from liblaf.pretty._config import PrettyConfigState, PrettyOptions, config
from liblaf.pretty._lower import LowerContext, TracedLeaf

_DEFAULT_TYPENAMES: dict[type, str] = {dict: "", list: "", set: "", tuple: ""}


@attrs.define
class TraceContext(contextlib.AbstractContextManager):
    config: PrettyConfigState = attrs.field(factory=config.dump, kw_only=True)
    level: int = attrs.field(default=0, kw_only=True)
    _highlighter: Highlighter | None = attrs.field(
        factory=ReprHighlighter, kw_only=True
    )
    _obj_id_counter: Counter[int] = attrs.field(factory=Counter)
    _typenames: Mapping[type, str] = attrs.field(default=_DEFAULT_TYPENAMES)
    _types: set[type] = attrs.field(factory=set)

    @classmethod
    def from_options(cls, **kwargs: Unpack[PrettyOptions]) -> Self:
        with config.override(**kwargs) as cfg:
            return cls(config=cfg.dump())

    def __enter__(self) -> Self:
        self.level += 1
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
        /,
    ) -> None:
        self.level -= 1

    def highlight(self, text: str) -> TracedLeaf:
        if self._highlighter is None:
            return TracedLeaf(Text(text))
        return TracedLeaf(self._highlighter(text))

    def lower(self) -> LowerContext:
        return LowerContext(
            obj_id_counter=self._obj_id_counter,
            typenames=self._disambiguate_typenames(),
        )

    def repr(self, obj: object) -> TracedLeaf:
        text: str = self._arepr.repr1(obj, self.config.max_level - self.level)
        if _utils.has_ansi(text):
            return TracedLeaf(Text.from_ansi(text))
        if self._highlighter is None:
            return TracedLeaf(Text(text))
        return TracedLeaf(self._highlighter(text))

    def visit(self, obj: object) -> bool:
        obj_id: int = id(obj)
        visited: bool = obj_id in self._obj_id_counter
        self._obj_id_counter[obj_id] += 1
        self._types.add(type(obj))
        return visited

    @functools.cached_property
    def _arepr(self) -> reprlib.Repr:
        return reprlib.Repr(
            maxlevel=self.config.max_level,
            maxtuple=self.config.max_list,
            maxlist=self.config.max_list,
            maxarray=self.config.max_array,
            maxdict=self.config.max_dict,
            maxset=self.config.max_list,
            maxfrozenset=self.config.max_list,
            maxdeque=self.config.max_list,
            maxstring=self.config.max_string,
            maxlong=self.config.max_long,
            maxother=self.config.max_other,
            indent=self.config.indent.plain,
        )

    def _disambiguate_typenames(self) -> dict[type, str]:
        # TODO: make this algorithm smarter
        counter: Counter[str] = Counter()
        typenames: dict[type, str] = {**self._typenames}
        for cls in self._types:
            if cls in typenames:
                continue
            for name in _typenames(cls):
                counter[name] += 1
        for cls in self._types:
            if cls in typenames:
                continue
            names: list[str] = _typenames(cls)
            for name in names:
                if counter[name] == 1:
                    typenames[cls] = name
                    break
            else:
                typenames[cls] = names[-1]
        return typenames


def _typenames(cls: type) -> list[str]:
    module: str = getattr(cls, "__module__", "<unknown>")
    name: str = cls.__name__
    qualname: str | None = getattr(cls, "__qualname__", name)
    if qualname != name:
        return [name, qualname, f"{module}.{name}", f"{module}.{qualname}"]
    return [name, f"{module}.{name}"]
