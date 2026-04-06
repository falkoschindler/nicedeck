import contextvars as _contextvars

from .code import Code as code
from .code import CodeResult as code_result
from .code import Demo as demo
from .content import CenterColumn as center_column
from .content import CenterHeading as center_heading
from .content import CenterRow as center_row
from .content import Heading as heading
from .note import Note as note
from .step import Step as step

_overview_mode = _contextvars.ContextVar('_overview_mode', default=False)


def deck(**kwargs):
    if _overview_mode.get():
        from .overview import OverviewDeck
        return OverviewDeck(**kwargs)
    from ._deck import Deck
    return Deck(**kwargs)


def slide():
    if _overview_mode.get():
        from .overview import OverviewSlide
        return OverviewSlide()
    from ._slide import Slide
    return Slide()


def run(root, **kwargs):
    from nicegui import ui

    @ui.page('/overview')
    def _overview_page():
        _overview_mode.set(True)
        root()

    ui.run(root=root, **kwargs)


__all__ = [
    'center_column',
    'center_heading',
    'center_row',
    'code',
    'code_result',
    'deck',
    'demo',
    'heading',
    'note',
    'run',
    'slide',
    'step',
]
