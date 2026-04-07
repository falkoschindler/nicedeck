from __future__ import annotations

from typing import Self

from nicegui import ui

from ._deck import deck


class OverviewDeck(ui.column):
    """A deck rendered as a vertical overview of all slides with notes."""

    def __init__(self) -> None:
        super().__init__()
        self.classes('w-full items-center gap-16 py-8')
        ui.add_css('''
            .overview-slide [style*="opacity"] { opacity: 1 !important; }
            @media print {
                .overview-slide { break-before: page; }
                .overview-slide:first-child { break-before: avoid; }
            }
        ''')


class OverviewSlide(ui.column):
    """A slide rendered for overview/print mode with notes above the content."""

    def __init__(self) -> None:
        super().__init__()
        self.classes('w-full max-w-5xl overview-slide')
        self._notes_el: ui.column
        self._content_el: ui.element

    def __enter__(self) -> Self:
        super().__enter__()
        self._notes_el = ui.column().classes('w-full gap-0')
        self._content_el = ui.element('div')
        self._content_el.classes(
            'w-full aspect-video bg-[#fafbfc] dark:bg-[#0f1117]'
            ' relative overflow-hidden rounded-lg border shadow'
        )
        self._content_el.__enter__()
        return self

    def __exit__(self, *args) -> None:
        self._content_el.__exit__(*args)
        slide = deck.current_slide
        if slide.notes:
            with self._notes_el:
                ui.markdown(slide.notes)
        super().__exit__(*args)
