from typing import Callable

from .deck import Slide, deck
from nicegui import events, ui
import time


def run(*, time_limit: float = 0, setup: Callable | None = None, classes: str = '', props: str = '', **kwargs) -> None:

    @ui.page('/')
    def index():
        if setup:
            setup()

        carousel = ui.carousel().classes(classes).props(props).props('fullscreen navigation') \
            .bind_value_from(deck, 'slide_index', str)

        @carousel.on_value_change
        def _(e: events.ValueChangeEventArguments) -> None:
            deck.slide_index = int(e.value)
            deck.navigate.emit()

        @ui.keyboard
        def _(e: events.KeyEventArguments) -> None:
            if e.action.keydown and e.key.arrow_left:
                if deck.slide_step > 0:
                    deck.slide_step -= 1
                elif deck.slide_index > 0:
                    deck.slide_index -= 1
                    deck.slide_step = deck.current_slide.steps - 1
            if e.action.keydown and e.key.arrow_right:
                if deck.slide_step < deck.current_slide.steps - 1:
                    deck.slide_step += 1
                elif deck.slide_index < len(deck.slides) - 1:
                    deck.slide_index += 1
                    deck.slide_step = 0

        with carousel:
            for i, s in enumerate(deck.slides):
                Slide.rendering = s
                s.steps = 1
                with ui.carousel_slide(name=str(i)).style('padding: 0'):
                    s.func()
            Slide.rendering = None

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
            for s in deck.slides:
                Slide.rendering = s
                s.steps = 1
                with ui.column().classes('w-full max-w-5xl overview-slide'):
                    ui.markdown(s.notes)
                    with ui.card().props('bordered flat') \
                            .classes('w-full aspect-video bg-[#fafbfc] dark:bg-[#0f1117] relative overflow-hidden'):
                        s.func()
            Slide.rendering = None

    ui.run(**kwargs)
