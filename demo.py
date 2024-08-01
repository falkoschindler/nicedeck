#!/usr/bin/env python3
from nicegui import ui

import nicedeck as nd

with nd.deck(time_limit=10 * 60).props('control-color=blue-2') as deck:
    with nd.slide():
        nd.note('''
            Hello everyone! Welcome to my talk about **NiceDeck**.
        ''')
        ui.label('NiceDeck').classes('text-4xl absolute-center')

    with nd.slide():
        ui.link('Open speaker notes...', '/notes', new_tab=True).classes('absolute-center text-xl')

    with nd.slide():
        nd.center_heading('Part 1: Introduction')

    with nd.slide():
        nd.note('''
            NiceDeck is a Python package that makes it easy to create **beautiful** and **interactive** presentations.
        ''')
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

    with nd.slide():
        nd.center_heading('Part 2: Code Examples')

    with nd.slide():
        nd.note('''
            Let's see a simple code example.
        ''')
        nd.heading('Hello World')
        with ui.column().classes('absolute-center'):
            ui.code('''
                #!/usr/bin/env python3
                    
                print('Hello, Python world!')
            ''')

    with nd.slide():
        nd.note('''
            You can also include interactive NiceGUI elements.
        ''')
        nd.heading('NiceGUI Elements')
        with nd.center_row().classes('absolute-center'):
            @nd.demo
            def demo():
                ui.button('Click me!', on_click=lambda: ui.notify('You clicked me!'))

    with nd.slide():
        nd.center_heading('Part 3: End')

    with nd.slide():
        nd.note('''
            This concludes this small demo of NiceDeck.
        ''')
        with ui.column().classes('absolute-center items-center gap-16'):
            ui.label('You reached the end of this demo.').classes('text-4xl')
            ui.image('assets/face.png').classes('w-32')

ui.run(title='NiceDeck Demo Talk')
