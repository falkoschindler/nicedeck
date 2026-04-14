import time
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class Timer:
    limit: float
    reference_time: float | None = field(default=None, init=False)
    remaining: float | None = field(default=None, init=False)
    state: Literal['initial', 'running', 'paused'] = field(default='initial', init=False)

    @property
    def display(self) -> str:
        if self.reference_time is not None:
            return _format_time(self.reference_time - time.time())
        if self.remaining is not None:
            return _format_time(self.remaining)
        return _format_time(self.limit)

    def start(self) -> None:
        self.reference_time = time.time() + self.limit
        self.remaining = None
        self.state = 'running'

    def pause(self) -> None:
        if self.reference_time is not None:
            self.remaining = self.reference_time - time.time()
        self.reference_time = None
        self.state = 'paused'

    def resume(self) -> None:
        if self.remaining is not None:
            self.reference_time = time.time() + self.remaining
        self.remaining = None
        self.state = 'running'

    def reset(self) -> None:
        self.reference_time = None
        self.remaining = None
        self.state = 'initial'


def _format_time(seconds: float) -> str:
    sign = '-' if seconds < 0 else ''
    seconds = abs(int(seconds))
    return f'{sign}{seconds // 60:.0f}:{seconds % 60:02.0f}'
