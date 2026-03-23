#!/usr/bin/env python3
from contextlib import contextmanager
from typing import Generator

import nicedeck as nd
from nicegui import ui


def root():
    @contextmanager
    def slide(heading: str | None = None, *,
              center_heading: str | None = None,
              hide_navigation: bool = False) -> Generator[None, None, None]:
        with nd.slide():
            if heading:
                nd.heading(heading)
            if center_heading:
                nd.center_heading(center_heading)
            wedge = ui.label().classes('absolute -bottom-14 bg-[#eee] w-[120%] h-32 -rotate-[4deg]')
            if hide_navigation:
                wedge.classes('z-10 bg-white')
            else:
                ui.label().bind_text_from(deck, 'value', lambda v: v.split('_')[-1]) \
                    .classes('absolute bottom-4 right-4 text-gray-400')
            with nd.center_row():
                yield

    with nd.deck() as deck:
        with slide(heading='PyCon Germany 2026'):
            ui.label('Hi!')

        with slide(heading='Coming soon...'):
            ui.label('Coming soon...')


ui.run(root, title='PyCon Germany 2026')
