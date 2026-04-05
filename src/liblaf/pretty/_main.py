from rich.console import Console, RenderableType

from ._describe._api import describe
from ._lower._api import lower
from ._options import PrettyOptions
from ._trace._api import trace


def pdoc(obj: object, /, *, options: PrettyOptions | None = None) -> RenderableType:
    resolved: PrettyOptions = options or PrettyOptions()
    spec = describe(obj, resolved)
    traced = trace(spec, resolved)
    return lower(traced, resolved)


def pformat(
    obj: object,
    /,
    console: Console | None = None,
    *,
    options: PrettyOptions | None = None,
    soft_wrap: bool = True,
) -> str:
    resolved: PrettyOptions = options or PrettyOptions()
    console = _get_console(console, resolved)
    lowered = pdoc(obj, options=resolved)
    with console.capture() as capture:
        console.print(lowered, soft_wrap=soft_wrap)
    return capture.get()


def pprint(
    obj: object,
    /,
    console: Console | None = None,
    *,
    options: PrettyOptions | None = None,
    soft_wrap: bool = True,
) -> None:
    resolved: PrettyOptions = options or PrettyOptions()
    console = _get_console(console, resolved)
    lowered = pdoc(obj, options=resolved)
    console.print(lowered, soft_wrap=soft_wrap)


def _get_console(console: Console | None, options: PrettyOptions) -> Console:
    if console is not None:
        return console
    return Console(color_system=None, soft_wrap=True, width=options.max_width)
