from typing import Callable, List, Optional

from nicegui import ui

from ._deck import Deck
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

_slides: List[Callable] = []


def slide(func: Optional[Callable] = None) -> Callable:
    """Register a slide function. Can be used as @nd.slide or @nd.slide()."""
    def decorator(f: Callable) -> Callable:
        _slides.append(f)
        return f
    if func is not None:
        return decorator(func)
    return decorator


def run(*, time_limit: float = 0, setup: Optional[Callable] = None,
        deck_classes: str = '', deck_props: str = '', **kwargs) -> None:
    _deck: Optional[Deck] = None

    @ui.page('/')
    def index():
        nonlocal _deck
        if setup:
            setup()
        _deck = Deck()
        if deck_classes:
            _deck.classes(deck_classes)
        if deck_props:
            _deck.props(deck_props)
        with _deck:
            for fn in _slides:
                with Slide():
                    fn()

    @ui.page('/notes')
    def notes():
        if _deck is None:
            ui.label('Open the main page first')
            return
        ui.add_css('hr { border: 1px dashed gray }')
        _deck.timer(time_limit)
        ui.timer(1.0, _deck.timer.refresh)
        _deck.show_notes()

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
