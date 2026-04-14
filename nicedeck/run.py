from typing import Callable

from .deck import Slide, deck
from .timer import Timer
from nicegui import events, ui

NOTE_CLASSES = 'text-gray-400 [&_em]:text-black [&_em]:not-italic [&_em]:font-medium [&_code]:text-[90%]'


def run(*, time_limit: float = 0, setup: Callable | None = None, classes: str = '', props: str = '', **kwargs) -> None:
    timer = Timer(time_limit)

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

        with ui.row(align_items='center'):
            ui.label().classes('text-bold text-lg').bind_text_from(timer, 'display')
            for state, icon, action in [
                ('initial', 'play_arrow', timer.start),
                ('running', 'pause', timer.pause),
                ('paused', 'play_arrow', timer.resume),
                ('paused', 'replay', timer.reset),
            ]:
                ui.button(icon=icon, on_click=action).props('flat round') \
                    .bind_visibility_from(timer, 'state', value=state)

        @ui.refreshable
        def show_notes() -> None:
            ui.markdown(deck.current_slide.notes).classes(NOTE_CLASSES)

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
                    ui.markdown(s.notes).classes(NOTE_CLASSES)
                    with ui.card().props('bordered flat') \
                            .classes('w-full aspect-video bg-[#fafbfc] dark:bg-[#0f1117] relative overflow-hidden'):
                        s.func()
            Slide.rendering = None

    ui.run(**kwargs)
