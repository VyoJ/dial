"""dial - A Python library for procedural and declarative generation of analog clock faces."""

from dial.clock import Clock
from dial.element import Element
from dial.elements import Face, Hands, Numerals, Overlay, Ticks

__version__ = "0.1.0"
__all__ = ["Clock", "Element", "Face", "Ticks", "Numerals", "Hands", "Overlay"]


def hello() -> str:
    """Return a friendly greeting from the dial library."""
    return "Hello from dial!"
