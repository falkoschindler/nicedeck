#!/usr/bin/env python3
from contextlib import contextmanager
from pathlib import Path

from nicegui import app, ui

import nicedeck as nd

PATH = Path(__file__).parent
ui.add_head_html(f'<style>{(PATH / "style.css").read_text()}</style>')
app.add_static_files('/fonts', PATH / 'fonts')
FACE_SVG = (PATH / 'assets' / 'half_face.svg').read_text()


@contextmanager
def slide(*, hide_navigation: bool = False) -> None:
    with nd.slide():
        wedge = ui.label().classes('absolute -bottom-14 bg-[#eee] w-[120%] h-32 -rotate-[4deg]')
        if hide_navigation:
            wedge.classes('z-10 bg-white')
        yield


with nd.deck(time_limit=30 * 60):
    with slide(hide_navigation=True):
        with ui.column().classes('absolute-left'):
            ui.html(FACE_SVG).classes('w-[40vh] my-auto')
        with ui.column().classes('absolute-center w-full ml-[30vw]'):
            ui.markdown('*NiceGUI*').classes('text-5xl font-medium mt-12')
            ui.label('Inventing Python’s Nicest UI Framework').classes('text-4xl text-gray-800')
            with ui.row().classes('gap-8 mt-12'):
                ui.label('Falko Schindler').classes('text-lg text-gray-600')
                with ui.row().classes('gap-2 items-center'):
                    ui.image('assets/zauberzeug-logo.png').classes('w-6 h-6 opacity-70')
                    ui.label('zauberzeug.com').classes('text-lg text-gray-600')
                with ui.row().classes('gap-2 items-center'):
                    ui.html((Path(__file__).parent / 'assets' / 'github.svg').read_text()).classes('opacity-70')
                    ui.label('github.com/zauberzeug').classes('text-lg text-gray-600')

    with slide():
        nd.heading('Background')
        nd.note('''
            - Who am I, what is Zauberzeug?
            [HQ picture]
            [robots]
            - Core problem at Zauberzeug: Developing and controlling robots locally and remotely
        ''')

    with slide():
        nd.center_heading('A New UI Framework')

    with slide():
        nd.heading('ODrive GUI')
        nd.note('''
            https://discourse.odriverobotics.com/uploads/default/original/2X/6/6eb090388d280ab70d14bc507b08dbe186ac7a90.png
        ''')

    with slide():
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

    with slide():
        nd.heading('Idea')
        nd.note('''
            - new UI toolbox based on a Flask/FastAPI app serving an Angular frontend?
            - more Pythonic than Streamlit
            - proof of concept after a few hours
        ''')

    with slide():
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

    with slide():
        nd.heading('NiceGUI')
        nd.note('''
            - The name "NiceGUI":
            - Our framework should be "nice" to use.
            - Nice guy:
                "a man who puts the needs of others before his own, avoids confrontations, does favors, provides emotional support, tries to stay out of trouble, and generally acts nicely towards others"
                https://en.wikipedia.org/wiki/Nice_guy
            - Pronounce as "nice guy"
        ''')

    with slide():
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

    with slide():
        nd.heading('Hierarchical Layout')
        nd.note('Pythonic way to create hierarchy? Indentation!')
        with nd.center_row():
            @nd.demo
            def demo():
                with ui.card():
                    with ui.row():
                        ui.label('Hello')
                        ui.label('world!')

    with slide():
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

    with slide():
        nd.heading('Event Handling: Embrace Lambdas')
        nd.note('''
            How to react on user input?
            --> lambda-friendly event registration
        ''')
        with nd.center_row():
            @nd.demo
            def demo():
                ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))

    with slide():
        nd.heading('Event Handling: With/without Arguments')
        with nd.center_row():
            @nd.demo
            def demo():
                ui.number(value=41, on_change=lambda e: ui.notify(f'new value: {e.value}'))

    with slide():
        nd.heading('Event Handling: Auto-Context')
        with nd.center_row():
            @nd.demo
            def demo():
                with ui.card():
                    ui.button('Spawn', on_click=lambda: ui.label("I'm here!"))

    with slide():
        nd.heading('Event Handling: Sync/Async')
        with nd.center_row():
            @nd.demo
            def demo():
                async def handle_click():
                    ui.notify('Clicked!')

                ui.button('Click me', on_click=handle_click)

    with slide():
        nd.heading('Event Handling: Async Lambdas')
        with nd.center_row():
            @nd.demo
            def demo():
                async def notify(value):
                    ui.notify(f'New value: {value}')

                ui.number(value=12, on_change=lambda e: ui.notify(f'New value: {e.value}'))

    with slide():
        nd.heading('Builder Pattern')
        with nd.center_row():
            @nd.demo
            def demo():
                ui.button('Nice!', icon='face') \
                    .props('outline') \
                    .classes('absolute-center') \
                    .style('box-shadow: 0 0 1rem 0 rgba(0, 127, 255, 0.25)')

    with slide():
        nd.heading('Leaking Abstractions')
        nd.note('''
            - Quasar props
            - other Quasar elements
            - Tailwind classes
            - CSS
            - JavaScript
            - HTML
        ''')

    with slide():
        nd.heading('Tailwind API')
        with nd.center_row():
            @nd.demo
            def demo():
                ui.label('TailwindCSS') \
                    .tailwind \
                    .text_color('blue-600') \
                    .border_width('4') \
                    .border_style('dashed') \
                    .border_color('blue-600') \
                    .padding('p-4')

    with slide():
        nd.heading('Binding')
        with nd.center_row():
            @nd.demo
            def demo():
                number = ui.number(value=42)

                ui.label().bind_text_from(number, 'value', lambda v: f'Value: {v}')

                ui.slider(min=0, max=100).bind_value(number)

    with slide():
        nd.heading('Refreshable UI')
        with nd.center_row():
            @nd.demo
            def demo():
                @ui.refreshable
                def print_temperature():
                    if slider.value < 0:
                        ui.label(f'Freezing: {slider.value}°C').classes('text-blue')
                    elif slider.value < 10:
                        ui.label(f'Cold: {slider.value}°C').classes('text-green')
                    else:
                        ui.label(f'Warm: {slider.value}°C').classes('text-orange')

                slider = ui.slider(value=0, min=-10, max=20, on_change=print_temperature.refresh)
                print_temperature()

    with slide():
        nd.heading('Refreshable UI with UI State')
        with nd.center_row():
            @nd.demo
            def demo():
                @ui.refreshable
                def show_counter():
                    count, set_count = ui.state(0)
                    ui.label(f'Counter: {count}')
                    ui.button('Increment', on_click=lambda: set_count(count + 1))

                show_counter()

    with slide():
        nd.heading('Markdown and HTML')
        with nd.center_row():
            @nd.demo
            def demo():
                ui.markdown('''
                    This is **Markdown**.
                ''')
                ui.html('''
                    <p>This is <strong>HTML</strong>.</p>
                ''')

    with slide():
        nd.heading('Markdown and HTML - Intelligent Indentation')
        with nd.center_row():
            @nd.demo
            def demo():
                with ui.card():
                    ui.markdown('''
                        This is **Markdown**.
                    ''')
                    ui.html('''
                        <p>This is <strong>HTML</strong>.</p>
                    ''')

    with slide():
        with ui.column().classes('absolute-center'):
            ui.markdown('### Applications')
            ui.link('zauberzeug.com', 'https://zauberzeug.com')
            ui.link('nicegui.io', 'https://nicegui.io')

ui.run(title='PyCon Ireland 2023',
       uvicorn_reload_includes='*.py, *.css')
