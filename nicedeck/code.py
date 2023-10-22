from nicegui import ui


class Code(ui.code):
    """A code block."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self._classes.append('p-2')
        self.copy_button.set_visibility(False)


class CodeResult(ui.element):
    """Rendered NiceGUI code."""

    def __init__(self, code: Code) -> None:
        super().__init__()

        BAR_COLOR = '#00000010'
        COLOR = '#ffffff'
        with ui.card().classes(f'no-wrap bg-[{COLOR}] rounded-xl p-0 gap-0') \
                .style('box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)'):
            with ui.row().classes(f'w-full h-8 p-2 bg-[{BAR_COLOR}]'):
                with ui.row().classes('gap-1 relative left-[1px] top-[1px]'):
                    ui.icon('circle').classes('text-[13px] text-red-400')
                    ui.icon('circle').classes('text-[13px] text-yellow-400')
                    ui.icon('circle').classes('text-[13px] text-green-400')
                with ui.row().classes('gap-0'):
                    with ui.label().classes(f'w-2 h-[24px] bg-[{COLOR}]'):
                        ui.label().classes(f'w-full h-full bg-[{BAR_COLOR}] rounded-br-[6px]')
                    with ui.row().classes(f'text-sm text-gray-600 dark:text-gray-400 px-6 py-1 h-[24px] rounded-t-[6px] bg-[{COLOR}] items-center gap-2'):
                        ui.label('NiceGUI')
                    with ui.label().classes(f'w-2 h-[24px] bg-[{COLOR}]'):
                        ui.label().classes(f'w-full h-full bg-[{BAR_COLOR}] rounded-bl-[6px]')
            with ui.column().classes('w-60 h-40 p-4 overflow-auto'):
                exec(code.content)  # pylint: disable=exec-used