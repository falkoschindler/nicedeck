from dataclasses import dataclass, field
from typing import Callable

from nicegui import Event


@dataclass
class Slide:
    """Data object representing a slide in a deck."""
    func: Callable[[], None]
    notes: str = ''
    step: int = field(default=0, init=False)
    steps: int = field(default=1, init=False)

    def reset(self) -> None:
        self.step = 0
        self.steps = 1


@dataclass
class Deck:
    """Data object holding all slides, current index, and navigate event."""
    slides: list[Slide] = field(default_factory=list)
    index: int = 0
    navigate: Event = field(default_factory=Event[[]])

    @property
    def current_slide(self) -> Slide:
        return self.slides[self.index]


deck = Deck()
