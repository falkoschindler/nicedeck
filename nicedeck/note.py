from dataclasses import dataclass

from .slide import Slide


@dataclass
class Note:
    text: str

    def __post_init__(self) -> None:
        assert Slide.current is not None, 'Note() must be used inside a slide'
        Slide.current.notes.append(self)
