from dataclasses import dataclass, field

from nicegui import Event

from ._slide import Slide


@dataclass
class Deck:
    """Data object holding all slides, current index, and navigate event."""
    slides: list[Slide] = field(default_factory=list)
    index: int = 0
    navigate: Event = field(default_factory=lambda: Event[[]]())

    @property
    def current_slide(self) -> Slide:
        return self.slides[self.index]


deck = Deck()
