#!/usr/bin/env python3
from pathlib import Path

from nicegui import app, ui

import nicedeck as nd

PATH = Path(__file__).parent
ui.add_head_html(f'<style>{(PATH / "style.css").read_text()}</style>')
app.add_static_files('/fonts', PATH / 'fonts')
FACE_SVG = (PATH / 'assets' / 'half_face.svg').read_text()

with nd.deck():
    with nd.slide():
        with ui.column().classes('absolute-left'):
            ui.html(FACE_SVG).classes('w-[40vh] my-auto')
        with ui.column().classes('absolute-center w-full ml-[30vw]'):
            ui.markdown('*NiceGUI*').classes('text-7xl font-medium mt-72')
            ui.label('Inventing Python’s Nicest UI Framework').classes('text-5xl text-gray-800')
            with ui.row().classes('gap-8 mt-24'):
                ui.label('Falko Schindler').classes('text-2xl text-gray-600')
                with ui.row().classes('gap-2 items-center'):
                    ui.image('assets/zauberzeug-logo.png').classes('w-6 h-6 opacity-70')
                    ui.label('zauberzeug.com').classes('text-2xl text-gray-600')
                with ui.row().classes('gap-2 items-center'):
                    ui.html((Path(__file__).parent / 'assets' / 'github.svg').read_text()).classes('opacity-70')
                    ui.label('github.com/zauberzeug').classes('text-2xl text-gray-600')

    with nd.slide():
        nd.heading('Background')
        nd.note('''
            - Who am I, what is Zauberzeug?
            [HQ picture]
            [robots]
            - Core problem at Zauberzeug: Developing and controlling robots locally and remotely
        ''')

    with nd.slide():
        nd.center_heading('A New UI Framework')

    with nd.slide():
        nd.heading('ODrive GUI')
        nd.note('''
            https://discourse.odriverobotics.com/uploads/default/original/2X/6/6eb090388d280ab70d14bc507b08dbe186ac7a90.png
        ''')

    with nd.slide():
        nd.heading('Streamlit')
        with nd.center_row():
            nd.code('''
                import streamlit as st

                st.write('Hello world!')
            ''')
            nd.code('''
                import streamlit as st

                if st.button('Say hello'):
                    st.write('Hi!')
            ''')
            nd.note('But: constant reload, hard to manage state, hard to create something like timers')

    with nd.slide():
        nd.heading('Idea')
        nd.note('''
            - new UI toolbox based on a Flask/FastAPI app serving an Angular frontend?
            - more Pythonic than Streamlit
            - proof of concept after a few hours
        ''')

    with nd.slide():
        nd.heading('JustPy')
        nd.note('''
            - Name? Just Python --> "JustPy"?
            - https://justpy.io/
            - (almost) exactly what we were looking for
                (but with Vue instead of Angular (why not) and based on Quasar and Tailwind)
            - used as a basis for version 0.x
            - removed in 1.0
                (code base in poor condition, deprecated Vue and Quasar versions, too much overhead)
        ''')

    with nd.slide():
        nd.heading('NiceGUI')
        nd.note('''
            - The name "NiceGUI":
            - Our framework should be "nice" to use.
            - Nice guy:
                "a man who puts the needs of others before his own, avoids confrontations, does favors, provides emotional support, tries to stay out of trouble, and generally acts nicely towards others"
                https://en.wikipedia.org/wiki/Nice_guy
            - Pronounce as "nice guy"
        ''')

    with nd.slide():
        nd.heading('Three-line Hello World')
        with nd.center_row():
            @nd.demo
            def demo():
                ui.label('Hello world!')
        nd.note('''
            - no command line tool to run
            - no build step
            - browser opens automatically
            - easy for sharing code examples for documentation and Q&A
        ''')

    with nd.slide():
        nd.heading('Hierarchical Layout')
        nd.note('Pythonic way to create hierarchy? Indentation!')
        with nd.center_row():
            @nd.demo
            def demo():
                with ui.card():
                    with ui.row():
                        ui.label('Hello')
                        ui.label('world!')

    with nd.slide():
        nd.heading('Hierarchical Layout: Embrace Indentation')
        with nd.center_row():
            with nd.step(0):
                ui.label('HTML').classes('text-2xl text-gray-600')
                nd.code('''
                    <div id="container">
                        <div id="box">
                            <p>Hello world!</p>
                        </div>
                    </div>
                ''', language='html')
            with nd.step():
                ui.label('NiceGUI').classes('text-2xl text-gray-600')
                nd.code('''
                    with ui.card():
                        with ui.row():
                            ui.label('Hello world!')
                ''').classes('flex-grow')
            with nd.step():
                ui.label('JustPy').classes('text-2xl text-gray-600')
                nd.code('''
                    container = Div()
                    box = Div()
                    label = Div(text='Hello world!')
                    box.add(label)
                    container.add(box)
                ''')

    with nd.slide():
        nd.heading('Event Handling: Embrace Lambdas')
        nd.note('''
            How to react on user input?
            --> lambda-friendly event registration
        ''')
        with nd.center_row():
            @nd.demo
            def demo():
                ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))

    with nd.slide():
        nd.heading('Event Handling: With/without Arguments')
        with nd.center_row():
            @nd.demo
            def demo():
                ui.number(value=41, on_change=lambda e: ui.notify(f'new value: {e.value}'))

    with nd.slide():
        nd.heading('Event Handling: Auto-Context')
        with nd.center_row():
            @nd.demo
            def demo():
                with ui.card():
                    ui.button('Spawn', on_click=lambda: ui.label("I'm here!"))

    with nd.slide():
        nd.heading('Event Handling: Sync/Async')
        with nd.center_row():
            @nd.demo
            def demo():
                async def handle_click():
                    ui.notify('Clicked!')

                ui.button('Click me', on_click=handle_click)

    with nd.slide():
        nd.heading('Event Handling: Async Lambdas')
        with nd.center_row():
            @nd.demo
            def demo():
                async def notify(value):
                    ui.notify(f'New value: {value}')

                ui.number(value=12, on_change=lambda e: ui.notify(f'New value: {e.value}'))

    with nd.slide():
        nd.heading('Builder Pattern')
        # TODO: style, classes, props

    with nd.slide():
        nd.heading('Leaking Abstractions')
        nd.note('''
            - Quasar props
            - other Quasar elements
            - Tailwind classes
            - CSS
            - HTML
        ''')

    with nd.slide():
        nd.heading('Tailwind API')

    with nd.slide():
        nd.heading('Binding')

    with nd.slide():
        nd.heading('"Refreshable" UI')

    with nd.slide():
        nd.heading('Markdown')

    with nd.slide():
        with ui.column().classes('absolute-center'):
            ui.markdown('### Applications')
            ui.link('zauberzeug.com', 'https://zauberzeug.com')
            ui.link('nicegui.io', 'https://nicegui.io')

ui.run(title='PyCon Ireland 2023')
