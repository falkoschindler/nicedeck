from nicegui import ui


class Heading(ui.label):
    """A heading for a slide."""

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.classes('absolute top-8 left-8 text-4xl text-gray-800 font-bold')


class CenterRow(ui.row):
    """A row centered on the slide."""

    def __init__(self) -> None:
        super().__init__()
        self.classes('w-full h-full content-center items-stretch justify-center')


class CenterColumn(ui.column):
    """A row centered on the slide."""

    def __init__(self) -> None:
        super().__init__()
        self.classes('w-full h-full content-center items-stretch justify-center')
