#!/usr/bin/env python3
from nicegui import ui

import nicedeck as nd


@nd.slide('''
    Hello everyone! Welcome to my talk about **NiceDeck**.
''')
def _():
    ui.label('NiceDeck').classes('text-4xl absolute-center')


@nd.slide()
def _():
    ui.link('Open speaker notes...', '/notes', new_tab=True).classes('absolute-center text-xl')


@nd.slide()
def _():
    nd.center_heading('Part 1: Introduction')


@nd.slide('''
    NiceDeck is a Python package that makes it easy to create **beautiful** and **interactive** presentations.
''')
def _():
    nd.heading('Features')
    with ui.column().classes('absolute-center text-xl'):
        with nd.step():
            ui.markdown('- Create slideshows in Python.')
        with nd.step():
            ui.markdown('- Include Markdown, images, and code.')
        with nd.step():
            ui.markdown('- Unveil parts of the slide step by step.')
        with nd.step():
            ui.markdown('- Interact with NiceGUI code examples directly in the slides.')
        with nd.step():
            ui.markdown('- View synchronized speaker notes on another screen or mobile device.')
        with nd.step():
            ui.markdown('- Use a countdown timer on the notes page.')


@nd.slide()
def _():
    nd.center_heading('Part 2: Code Examples')


@nd.slide('''
    Let's see a simple code example.
''')
def _():
    nd.heading('Hello World')
    with ui.column().classes('absolute-center'):
        ui.code('''
            #!/usr/bin/env python3

            print('Hello, Python world!')
        ''')


@nd.slide('''
    You can also include interactive NiceGUI elements.
''')
def _():
    nd.heading('NiceGUI Elements')
    with nd.center_row().classes('absolute-center'):
        @nd.demo
        def demo():
            ui.button('Click me!', on_click=lambda: ui.notify('You clicked me!'))


@nd.slide()
def _():
    nd.center_heading('Part 3: End')


@nd.slide('''
    This concludes this small demo of NiceDeck.
''')
def _():
    with ui.column().classes('absolute-center items-center gap-16'):
        ui.label('You reached the end of this demo.').classes('text-4xl')


nd.run(time_limit=10 * 60, props='control-color=blue-2', title='NiceDeck Demo Talk')
