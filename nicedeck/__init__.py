import time
from typing import Callable

from nicegui import app, ui

from ._deck import Deck
from ._event import NAVIGATE
from ._slide import Slide
from .code import Code as code
from .code import CodeResult as code_result
from .code import Demo as demo
from .content import CenterColumn as center_column
from .content import CenterHeading as center_heading
from .content import CenterRow as center_row
from .content import Heading as heading
from .note import Note as note
from .overview import OverviewDeck, OverviewSlide
from .step import Step as step

_slides: list[Callable] = []
_notes: list[list[str]] = []


def slide(func: Callable | None = None) -> Callable:
    """Register a slide function. Can be used as @nd.slide or @nd.slide()."""
    def decorator(f: Callable) -> Callable:
        _slides.append(f)
        return f
    if func is not None:
        return decorator(func)
    return decorator


def run(*, time_limit: float = 0, setup: Callable | None = None, classes: str = '', props: str = '', **kwargs) -> None:

    @ui.page('/')
    def index():
        if setup:
            setup()
        deck = Deck().classes(classes).props(props)
        with deck:
            for fn in _slides:
                with Slide():
                    fn()
        _notes[:] = [[n.text for n in child.notes] for child in deck.default_slot.children if isinstance(child, Slide)]

    @ui.page('/notes')
    def notes():
        if not _notes:
            ui.label('Open the main page first')
            return

        ui.add_css('hr { border: 1px dashed gray }')
        reference_time: float | None = None

        @ui.refreshable
        def show_timer() -> None:
            nonlocal reference_time
            with ui.row().classes('items-center text-bold text-lg'):
                if reference_time is None:
                    def start():
                        nonlocal reference_time
                        reference_time = int(time.time() + time_limit)
                    ui.label(f'{time_limit // 60:.0f}:{time_limit % 60:02.0f}')
                    ui.button('Start', icon='play_arrow', on_click=start).props('flat')
                else:
                    dt = reference_time - time.time()
                    ui.label(f'{"-" if dt < 0 else ""}{abs(dt) // 60:.0f}:{abs(dt) % 60:02.0f}')

        @ui.refreshable
        def show_notes() -> None:
            slide_name = app.storage.general.get('slide_name', 'slide_1')
            idx = int(slide_name.split('_')[1]) - 1
            if 0 <= idx < len(_notes):
                with ui.column().classes('gap-0'):
                    for text in _notes[idx]:
                        ui.markdown(text).classes('text-xl')

        if time_limit:
            show_timer()
            ui.timer(1.0, show_timer.refresh)
        show_notes()
        NAVIGATE.subscribe(show_notes.refresh)

    @ui.page('/overview')
    def overview():
        if setup:
            setup()
        with OverviewDeck():
            for fn in _slides:
                with OverviewSlide():
                    fn()

    ui.run(**kwargs)


__all__ = [
    'center_column',
    'center_heading',
    'center_row',
    'code',
    'code_result',
    'demo',
    'heading',
    'note',
    'run',
    'slide',
    'step',
]
