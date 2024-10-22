import time
from typing import Optional

from nicegui import app, events, ui

from .slide import Slide


class Deck(ui.carousel):
    """A deck of slides."""

    def __init__(self, *, time_limit: float = 0) -> None:
        super().__init__(on_value_change=self.show_notes.refresh)
        self._props['fullscreen'] = True
        self._props['navigation'] = True
        self.bind_value(app.storage.general, 'slide_name')
        ui.keyboard(self._handle_key)
        self.reference_time: Optional[float] = None

        @ui.page('/notes')
        def notes() -> None:
            ui.add_head_html('<style>hr { border: 1px dashed gray }</style>')
            self.timer(time_limit)
            ui.timer(1.0, self.timer.refresh)
            self.show_notes()

    @ui.refreshable_method
    def show_notes(self) -> None:
        with ui.column().classes('gap-0'):
            for note in self.slide.notes:
                ui.markdown(note.text).classes('text-xl')

    @ui.refreshable_method
    def timer(self, time_limit: float) -> None:
        with ui.row().classes('items-center text-bold text-lg'):
            if self.reference_time is None:
                def start_timer() -> None:
                    self.reference_time = int(time.time() + time_limit)
                ui.label(f'{time_limit // 60:.0f}:{time_limit % 60:02.0f}')
                ui.button('Start', icon='play_arrow', on_click=start_timer).props('flat')
            else:
                dt = self.reference_time - time.time()
                ui.label(f'{"-" if dt < 0 else ""}{abs(dt) // 60:.0f}:{abs(dt) % 60:02.0f}')

    @property
    def slide(self) -> Slide:
        """The currently visible slide."""
        index = int(self.value.split('_')[1]) - 1
        element = self.default_slot.children[index]
        assert isinstance(element, Slide)
        return element

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
