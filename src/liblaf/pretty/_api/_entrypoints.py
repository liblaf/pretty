from typing import Any

import rich
from rich.console import Console

from .._lower import lower
from .._trace import trace
from ._config import PrettyOptions, config
from ._doc import PrettyDoc


def pdoc(obj: Any, *, options: PrettyOptions | None = None, **kwargs: Any) -> PrettyDoc:
    resolved: PrettyOptions = _resolve_options(options, kwargs)
    traced = trace(obj, options=resolved)
    return lower(traced, options=resolved)


def pformat(
    obj: Any,
    console: Console | None = None,
    *,
    options: PrettyOptions | None = None,
    soft_wrap: bool = True,
    **kwargs: Any,
) -> str:
    resolved: PrettyOptions = _resolve_options(options, kwargs)
    console = _get_console(console, resolved)
    pretty_doc: PrettyDoc = pdoc(obj, options=resolved)
    with console.capture() as capture:
        console.print(pretty_doc, soft_wrap=soft_wrap)
    return capture.get()


def pprint(
    obj: Any,
    console: Console | None = None,
    *,
    options: PrettyOptions | None = None,
    soft_wrap: bool = True,
    **kwargs: Any,
) -> None:
    resolved: PrettyOptions = _resolve_options(options, kwargs)
    console = _get_console(console, resolved)
    pretty_doc: PrettyDoc = pdoc(obj, options=resolved)
    console.print(pretty_doc, soft_wrap=soft_wrap)


def _resolve_options(
    options: PrettyOptions | None, overrides: dict[str, Any]
) -> PrettyOptions:
    base: PrettyOptions = config.get() if options is None else options
    if overrides:
        return base.replace(**overrides)
    return base


def _get_console(console: Console | None, options: PrettyOptions) -> Console:
    if console is not None:
        return console
    return Console(color_system=None, soft_wrap=True, width=options.max_width)
