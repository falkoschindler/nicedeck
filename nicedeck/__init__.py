import time
from typing import Callable

from nicegui import app, events, ui

from ._deck import Slide, deck
from .code import Code as code
from .code import CodeResult as code_result
from .code import Demo as demo
from .content import CenterColumn as center_column
from .content import CenterHeading as center_heading
from .content import CenterRow as center_row
from .content import Heading as heading
from .step import Step as step


def slide(notes: str = '') -> Callable:
    """Register a slide function. Can be used as @nd.slide or @nd.slide(notes='...')."""
    def decorator(f: Callable) -> Callable:
        deck.slides.append(Slide(f, notes))
        return f
    return decorator


def run(*, time_limit: float = 0, setup: Callable | None = None, classes: str = '', props: str = '', **kwargs) -> None:

    @ui.page('/')
    def index():
        if setup:
            setup()

        carousel = ui.carousel().classes(classes).props(props).props('fullscreen navigation') \
            .bind_value(app.storage.general, 'slide_name')

        @carousel.on_value_change
        def _(e: events.ValueChangeEventArguments) -> None:
            deck.index = int(e.value.split('_')[1]) - 1
            deck.navigate.emit()

        @ui.keyboard
        def _(e: events.KeyEventArguments) -> None:
            s = deck.current_slide
            if e.action.keydown and e.key.arrow_left:
                if s.step > 0:
                    s.step -= 1
                else:
                    carousel.previous()
            if e.action.keydown and e.key.arrow_right:
                if s.step < s.steps - 1:
                    s.step += 1
                else:
                    carousel.next()

        with carousel:
            for i, s in enumerate(deck.slides):
                deck.index = i
                s.reset()
                with ui.carousel_slide().style('padding: 0'):
                    s.func()

    @ui.page('/notes')
    def notes():
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
            ui.markdown(deck.current_slide.notes).classes('text-xl')

        if time_limit:
            show_timer()
            ui.timer(1.0, show_timer.refresh)
        show_notes()
        deck.navigate.subscribe(show_notes.refresh)

    @ui.page('/overview')
    def overview():
        if setup:
            setup()
        ui.add_css('''
            .overview-slide [style*="opacity"] { opacity: 1 !important; }
            @media print {
                .overview-slide { break-before: page; }
                .overview-slide:first-child { break-before: avoid; }
            }
        ''')
        with ui.column().classes('w-full items-center gap-16 py-8'):
            for i, s in enumerate(deck.slides):
                deck.index = i
                s.reset()
                with ui.column().classes('w-full max-w-5xl overview-slide'):
                    ui.markdown(s.notes)
                    with ui.card().props('bordered flat') \
                            .classes('w-full aspect-video bg-[#fafbfc] dark:bg-[#0f1117] relative overflow-hidden'):
                        s.func()

    ui.run(**kwargs)


__all__ = [
    'center_column',
    'center_heading',
    'center_row',
    'code',
    'code_result',
    'demo',
    'heading',
    'run',
    'slide',
    'step',
]
