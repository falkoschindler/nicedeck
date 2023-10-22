from typing import Optional, Self

from nicegui import ui


class Slide(ui.carousel_slide):
    """A slide in a deck."""
    current: Optional[Self] = None

    def __init__(self) -> None:
        super().__init__()
        self._style['padding'] = '0'
        self.step = 0
        self.steps = 1

    def __enter__(self) -> Self:
        Slide.current = self
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        Slide.current = None
        super().__exit__(exc_type, exc_value, traceback)
