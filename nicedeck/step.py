from typing import Optional, cast

from nicegui import binding, ui

from .slide import Slide


class Step(ui.column):
    """A context manager for limiting the nested UI elements to certain slide steps."""
    visible = binding.BindableProperty(on_change=lambda sender, _: cast(Step, sender).handle_visibility_change())

    def __init__(self,
                 min: Optional[int] = None,  # pylint: disable=redefined-builtin
                 max: Optional[int] = None,  # pylint: disable=redefined-builtin
                 ) -> None:
        super().__init__()
        assert Slide.current is not None, 'Step() must be used inside a slide'
        if min != 0:
            Slide.current.steps += 1
        if min is None:
            min = Slide.current.steps - 1
        if max is None:
            max = 999
        self.bind_visibility_from(Slide.current, 'step', lambda s: min <= s <= max)

    def handle_visibility_change(self) -> None:
        """Called when the visibility of this step changes."""
        self.style(f'opacity: {1 if self.visible else 0.5}')
