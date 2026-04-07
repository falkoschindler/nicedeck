from nicegui import app, events, ui

from ._event import NAVIGATE
from ._slide import Slide


class Deck(ui.carousel):
    """A deck of slides."""

    def __init__(self) -> None:
        super().__init__(on_value_change=NAVIGATE.emit)
        self._props['fullscreen'] = True
        self._props['navigation'] = True
        self.bind_value(app.storage.general, 'slide_name')

        @ui.keyboard
        def _handle_key(e: events.KeyEventArguments) -> None:
            index = int(self.value.split('_')[1]) - 1
            slide: Slide = self.default_slot.children[index]  # type: ignore[assignment]
            if e.action.keydown and e.key.arrow_left:
                if slide.step > 0:
                    slide.step -= 1
                else:
                    self.previous()
            if e.action.keydown and e.key.arrow_right:
                if slide.step < slide.steps - 1:
                    slide.step += 1
                else:
                    self.next()
