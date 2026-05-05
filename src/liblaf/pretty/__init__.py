"""Public API for `liblaf.pretty`.

Import [`pformat`][liblaf.pretty.pformat] when you want plain text,
[`plower`][liblaf.pretty.plower] when you want the width-aware Rich renderable,
[`pprint`][liblaf.pretty.pprint] or [`pp`][liblaf.pretty.pp] when you want to
print immediately, and the registration helpers when you need to teach the
formatter about custom types.
"""

from lazy_loader import attach_stub

__getattr__, __dir__, __all__ = attach_stub(__name__, __file__)

del attach_stub
