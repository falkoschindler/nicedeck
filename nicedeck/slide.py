from collections.abc import Callable

from .deck import deck, Slide


def slide(notes: str = '') -> Callable:
    """Register a slide function. Can be used as @nd.slide or @nd.slide(notes='...')."""
    def decorator(f: Callable) -> Callable:
        deck.slides.append(Slide(f, notes))
        return f
    return decorator
