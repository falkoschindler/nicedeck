from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Slide:
    """Data object representing a slide in a deck."""
    func: Callable
    notes: str = ''
    step: int = field(default=0, init=False)
    steps: int = field(default=1, init=False)
