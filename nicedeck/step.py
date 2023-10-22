from typing import Optional

from nicegui import ui

from .slide import Slide


class Step(ui.element):
    """A context manager for limiting the nested UI elements to certain slide steps."""

    def __init__(self,
                 min: Optional[int] = None,  # pylint: disable=redefined-builtin
                 max: Optional[int] = None,  # pylint: disable=redefined-builtin
                 ) -> None:
        super().__init__()
        assert Slide.current is not None, 'Step() must be used inside a slide'
        Slide.current.steps += 1
        if min is None:
            min = Slide.current.steps - 1
        if max is None:
            max = float('inf')
        self.bind_visibility_from(Slide.current, 'step', lambda s: min <= s <= max)
