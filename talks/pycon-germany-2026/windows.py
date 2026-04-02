from collections.abc import Callable
import inspect
import isort
from pathlib import Path
import re
from typing import Literal

from nicegui import ui
from nicegui.elements.markdown import remove_indentation


def demo(f: Callable | None = None, *, mode: Literal['rows', 'cols'] = 'cols') -> Callable:
    """Render a callable as a demo with Python code and browser window."""
    def wrap(f: Callable) -> Callable:
        with ui.grid().classes(f'w-full max-w-[95vw] grid-{mode}-[auto_auto] gap-4 items-stretch'):
            code_window(_get_full_code(f), language='python')
            browser_window(f).classes('min-h-[10rem]')
        return f
    if f is not None:
        return wrap(f)
    return wrap


def code_window(code: str | Path, *, title: str | None = None, language: str = 'python') -> ui.column:
    """Create a window for code. If code is empty, returns the body column for use as context manager."""
    if isinstance(code, Path):
        code = code.read_text()
    with ui.column().classes('''
        rounded-xl gap-0 size-full min-w-0
        bg-[#f0f4f8] dark:bg-[#1e222c]
    ''') as window:
        if title:
            with ui.row().classes('''
                w-full px-4 h-12 shrink-0 gap-2 items-center
                text-[0.8125rem] text-[#7d8590] dark:text-[#6b737e]
                border-b border-b-[rgba(0,0,0,0.06)] dark:border-b-[rgba(255,255,255,0.08)]
            '''):
                ui.icon('face')
                ui.label(title)
        ui.markdown(f'````{language}\n{remove_indentation(code)}\n````') \
            .classes('w-full grow py-2 overflow-x-auto [&_pre]:px-4 [&_pre]:w-fit [&_pre]:min-w-full')
    return window


def browser_window(content: Callable) -> ui.column:
    """Create a browser window."""
    with ui.column().classes('''
        rounded-xl gap-0 size-full
        bg-[#ffffff] dark:bg-[#181b23]
        ring-1 ring-[rgba(0,0,0,0.06)] dark:ring-[rgba(255,255,255,0.08)]
    ''') as window:
        with ui.column().classes('size-full p-4'):
            content()
    return window


def _get_full_code(f: Callable) -> str:
    """Get the full code of a function as a string."""
    code = inspect.getsource(f).split('# END OF DEMO', 1)[0].strip().splitlines()
    code = [line for line in code if not line.endswith('# HIDE')]
    while not code[0].strip().startswith(('def', 'async def')):
        del code[0]
    del code[0]
    if code[0].strip().startswith('"""'):
        while code[0].strip() != '"""':
            del code[0]
        del code[0]
    non_empty_lines = [line for line in code if line.strip()]
    indentation = len(non_empty_lines[0]) - len(non_empty_lines[0].lstrip())
    code = [line[indentation:] for line in code]
    has_root_function = any(line.strip().startswith(('def root(', 'async def root(')) for line in code)
    code = ['from nicegui import ui'] + [re.sub(r'^(\s*)# ?', r'\1', line) for line in code]
    code = ['' if line == '#' else line for line in code]

    if has_root_function:
        code = [line for line in code if line.strip() != 'return root']

    if not code[-1].startswith('ui.run('):
        code.append('ui.run(root)' if has_root_function else 'ui.run()')

    code.insert(-1, '')  # ensure blank line before ui.run
    while code[-3] == '':
        code.pop(-3)  # avoid double blank line before ui.run

    return isort.code('\n'.join(code), no_sections=True, lines_after_imports=1)
