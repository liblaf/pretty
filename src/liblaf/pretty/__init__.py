"""Pretty-print Python objects as Rich renderables.

Most callers use [liblaf.pretty.pformat][] to build a renderable or
[liblaf.pretty.pprint][] to print directly to the active Rich console.
"""

from lazy_loader import attach_stub

__getattr__, __dir__, __all__ = attach_stub(__name__, __file__)

del attach_stub
