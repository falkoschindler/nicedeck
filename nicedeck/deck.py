from __future__ import annotations

from collections.abc import Callable

from dataclasses import dataclass, field

from nicegui import Event, app, binding


@dataclass
class Deck:
    """Data object holding all slides, current index, and navigate event."""
    slides: list[Slide] = field(default_factory=list)
    slide_index: int = app.storage.general.get('slide_index', 0)
    slide_step: int = app.storage.general.get('slide_step', 0)
    navigate: Event = field(default_factory=Event[[]])

    @property
    def current_slide(self) -> Slide:
        return self.slides[self.slide_index]

    def __post_init__(self) -> None:
        binding.bind_to(self, 'slide_index', app.storage.general, 'slide_index')
        binding.bind_to(self, 'slide_step', app.storage.general, 'slide_step')


@dataclass
class Slide:
    """Data object representing a slide in a deck."""
    func: Callable[[], None]
    notes: str = ''
    steps: int = field(default=1, init=False)


deck = Deck()
