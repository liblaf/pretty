"""Shared sentinels and identity helpers used by the formatting pipeline."""

from lazy_loader import attach_stub

__getattr__, __dir__, __all__ = attach_stub(__name__, __file__)

del attach_stub
