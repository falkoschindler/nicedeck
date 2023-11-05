from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Self

from nicegui import ui

if TYPE_CHECKING:
    from .note import Note


class Slide(ui.carousel_slide):
    """A slide in a deck."""
    current: Optional[Slide] = None

    def __init__(self) -> None:
        super().__init__()
        self._style['padding'] = '0'
        self.step = 0
        self.steps = 1
        self.notes: List[Note] = []

    def __enter__(self) -> Self:
        Slide.current = self
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        Slide.current = None
        super().__exit__(exc_type, exc_value, traceback)
