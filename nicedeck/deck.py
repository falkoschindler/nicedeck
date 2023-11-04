from nicegui import app, events, ui

from .slide import Slide


class Deck(ui.carousel):
    """A deck of slides."""

    def __init__(self) -> None:
        super().__init__()
        self._props['fullscreen'] = True
        self._props['navigation'] = True
        self._props['control-color'] = 'grey-4'
        self.bind_value(app.storage.general, 'slide_name')
        ui.keyboard(self._handle_key)

    @property
    def slide(self) -> Slide:
        """The currently visible slide."""
        index = int(self.value.split('_')[1]) - 1
        return self.default_slot.children[index]

    def _handle_key(self, e: events.KeyEventArguments) -> None:
        if e.action.keydown and e.key.arrow_left:
            if self.slide.step > 0:
                self.slide.step -= 1
            else:
                self.previous()
        if e.action.keydown and e.key.arrow_right:
            if self.slide.step < self.slide.steps - 1:
                self.slide.step += 1
            else:
                self.next()
