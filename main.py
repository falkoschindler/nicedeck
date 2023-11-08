#!/usr/bin/env python3
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from nicegui import app, ui

import nicedeck as nd

PATH = Path(__file__).parent
ui.add_head_html(f'<style>{(PATH / "style.css").read_text()}</style>')
app.add_static_files('/fonts', PATH / 'fonts')
app.add_static_files('/assets', PATH / 'assets')
FACE_SVG = (PATH / 'assets' / 'half_face.svg').read_text()


@contextmanager
def slide(heading: Optional[str] = None, *,
          center_heading: Optional[str] = None,
          hide_navigation: bool = False) -> None:
    with nd.slide():
        if heading:
            nd.heading(heading)
        if center_heading:
            nd.center_heading(center_heading)
        wedge = ui.label().classes('absolute -bottom-14 bg-[#eee] w-[120%] h-32 -rotate-[4deg]')
        if hide_navigation:
            wedge.classes('z-10 bg-white')
        with nd.center_row():
            yield


with nd.deck(time_limit=30 * 60):
    with slide(hide_navigation=True):
        nd.note('''
            Welcome to my talk about NiceGUI!
                
            It's a story about
                
            - how we had a problem at hand,
            - didn't find an existing solution,
            - decided to create our own,
            - and ended up with a pretty powerful UI framework that is just taking off in the Python community.
            
            And it's about the difference between
            
            - creating something that works,
            - and creating something that is a pleasure to use.
        ''')
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
        nd.note('''
            - first some background
            - my company: Zauberzeug, Münsterland, ~15 employees
            
            ---
            
            - develop hardware and software from an idea to a product
            - includes: electronics, mechanics, 3D printing, microcontrollers, software, and AI
            
            ---

            - autonomous cleaning robot
            
            ---

            - Zauberzeug Robot Brain: industrial PC based on NVIDIA Jetson, can control hardware, runs AI models
            
            ---
            
            - newest creation, Zauberzeug Field Friend: agricultural robot for weed control
        ''')
        with nd.heading():
            ui.image('assets/zauberzeug-logo.webp').classes('w-40')
        ui.image('assets/building.webp').classes('absolute-center w-full h-[60vh]')
        with nd.step(), nd.center_row():
            ui.image('assets/office.jpg').classes('absolute-center w-full h-[60vh]')
        with nd.center_row():
            with nd.step(), ui.card():
                ui.image('assets/brushing-bot.webp').classes('w-60 h-40 bg-white')
            with nd.step(), ui.card():
                ui.image('assets/robot-brain.webp').classes('w-60 h-40 bg-white')
            with nd.step(), ui.card():
                ui.image('assets/field-friend.webp').classes('w-60 h-40 bg-white')

    with slide('Philosophy'):
        nd.note('''
            - Zauberzeug: creating tools that feel like magic
            - software _and_ hardware
            - Arthur C. Clarke: "Any sufficiently advanced technology is indistinguishable from magic."
        ''')
        with ui.column().classes('items-center gap-16'):
            with ui.row():
                with ui.column().classes('items-center'):
                    ui.label('Zauber').classes('font-bold text-2xl')
                    ui.label('[ˈtsaʊ̯bər]').classes('text-grey text-xs')
                    ui.label('🪄').classes('text-4xl')
                    ui.label('"magic"')
                with ui.column().classes('items-center'):
                    ui.label('zeug').classes('font-bold text-2xl')
                    ui.label('[ˈt͡sɔʏ̯k]').classes('text-grey text-xs')
                    ui.label('🔨').classes('text-4xl')
                    ui.label('"tools"')
            with ui.column().classes('bg-gray-50 shadow p-4 items-end'):
                ui.label('“Any sufficiently advanced technology is indistinguishable from magic.”') \
                    .classes('text-primary text-xl')
                ui.label('-- Arthur C. Clarke').classes('text-xs text-gray-600')

    with slide(center_heading='A New UI Framework'):
        nd.note('''
            - after this background: Why a new framework?
        ''')

    with slide('ODrive Motor Controller'):
        nd.note('''
            - Core problem at Zauberzeug: Developing and controlling robots locally and remotely
            - Example: ODrive motor controller, used in our robots
            - needs configuration and tuning
            - comes with a powerful Python CLI, but (at that time) a poor GUI, tedious to use (_not nice_)
            - idea: can we use Streamlit to write a custom tuning UI?
            - important: network connection to robot, so we can tune the controller while the robot is running
        ''')
        ui.image('assets/odrive.jpg').classes('w-[30%]').props('fit=contain')
        with nd.step().classes('w-[60%]'):
            ui.image('assets/odrive-gui.png').props('fit=contain').classes('border shadow')

    with slide('Streamlit'):
        nd.note('''
            - UI framework for Python
            - popular for its simplicity
        ''')
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

    with slide('Idea'):
        nd.note('''
            - new UI toolbox based on a Flask/FastAPI app serving an Angular frontend?
            - more Pythonic than Streamlit
            - proof of concept after a few hours
        ''')

    with slide('JustPy'):
        nd.note('''
            - Name? Just Python --> "JustPy"?
            - https://justpy.io/
            - (almost) exactly what we were looking for
                (but with Vue instead of Angular (why not) and based on Quasar and Tailwind)
            - used as a basis for version 0.x
            - removed in 1.0
                (code base in poor condition, deprecated Vue and Quasar versions, too much overhead)
        ''')

    with slide('NiceGUI'):
        nd.note('''
            - The name "NiceGUI":
            - Our framework should be "nice" to use.
            - Nice guy:
                "a man who puts the needs of others before his own, avoids confrontations, does favors, provides emotional support, tries to stay out of trouble, and generally acts nicely towards others"
                https://en.wikipedia.org/wiki/Nice_guy
            - Pronounce as "nice guy"
        ''')

    with slide('Three-line Hello World'):
        @nd.demo
        def demo():
            ui.label('Hello world!')
        nd.note('''
            - no command line tool to run
            - no build step
            - browser opens automatically
            - easy for sharing code examples for documentation and Q&A
        ''')

    with slide('Hierarchical Layout'):
        nd.note('Pythonic way to create hierarchy? Indentation!')

        @nd.demo
        def demo():
            with ui.card():
                with ui.row():
                    ui.label('Hello')
                    ui.label('world!')

    with slide('Hierarchical Layout: Embrace Indentation'):
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

    with slide('Event Handling: Embrace Lambdas'):
        nd.note('''
            How to react on user input?
            --> lambda-friendly event registration
        ''')

        @nd.demo
        def demo():
            ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))

    with slide('Behind the Scenes'):
        with ui.column().classes('w-[30rem] items-stretch'):
            ui.chat_message('I\'d like to see "/".', avatar='assets/chrome.svg', sent=True)
            with nd.step().classes('items-stretch'):
                ui.chat_message('Here you go:\n<html>...<script />...<button />...</html>', avatar='assets/python.svg')
            with nd.step().classes('items-stretch'):
                ui.chat_message('Let\'s talk via SocketIO!', avatar='assets/chrome.svg', sent=True)
            with nd.step().classes('items-stretch'):
                ui.chat_message('Ok. I\'ll keep the connection open.', avatar='assets/python.svg')
            with nd.step().classes('items-stretch'):
                ui.chat_message('The user clicked the button "Click me"!', avatar='assets/chrome.svg', sent=True)
            with nd.step().classes('items-stretch'):
                ui.chat_message('Please show a notification: "Clicked!"', avatar='assets/python.svg')

        def click_demo():
            with nd.step(min=1).classes('items-stretch'):
                ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))
        nd.code_result(click_demo)

    with slide('Event Handling: With/without Arguments'):
        @nd.demo
        def demo():
            ui.number(value=41, on_change=lambda e: ui.notify(f'new value: {e.value}'))

    with slide('Event Handling: Auto-Context'):
        @nd.demo
        def demo():
            with ui.card():
                ui.button('Spawn', on_click=lambda: ui.label("I'm here!"))

    with slide('Event Handling: Sync/Async'):
        @nd.demo
        def demo():
            async def handle_click():
                ui.notify('Clicked!')

            ui.button('Click me', on_click=handle_click)

    with slide('Event Handling: Async Lambdas'):
        @nd.demo
        def demo():
            async def notify(value):
                ui.notify(f'New value: {value}')

            ui.number(value=12, on_change=lambda e: notify(e.value))

    with slide('Builder Pattern'):
        @nd.demo
        def demo():
            ui.button('Nice!', icon='face') \
                .props('outline') \
                .classes('absolute-center') \
                .style('box-shadow: 0 0 1rem 0 rgba(0, 127, 255, 0.25)')

    with slide('Tailwind API'):
        @nd.demo
        def demo():
            ui.label('TailwindCSS') \
                .tailwind \
                .text_color('blue-600') \
                .border_width('4') \
                .border_style('dashed') \
                .border_color('blue-600') \
                .padding('p-4')

    with slide('Binding'):
        @nd.demo
        def demo():
            number = ui.number(value=42)

            ui.label().bind_text_from(number, 'value', lambda v: f'Value: {v}')

            ui.slider(min=0, max=100).bind_value(number)

    with slide('Refreshable UI'):
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

    with slide('Refreshable UI with UI State'):
        @nd.demo
        def demo():
            @ui.refreshable
            def show_counter():
                count, set_count = ui.state(0)
                ui.label(f'Counter: {count}')
                ui.button('Increment', on_click=lambda: set_count(count + 1))

            show_counter()

    with slide('Markdown and HTML'):
        @nd.demo
        def demo():
            ui.markdown('''
                This is **Markdown**.
            ''')
            ui.html('''
                <p>This is <strong>HTML</strong>.</p>
            ''')

    with slide('Markdown and HTML - Intelligent Indentation'):
        @nd.demo
        def demo():
            with ui.card():
                ui.markdown('''
                    This is **Markdown**.
                ''')
                ui.html('''
                    <p>This is <strong>HTML</strong>.</p>
                ''')

    with slide('On the Shoulders of Giants'):
        def giant(name: str, note: str) -> None:
            with nd.step():
                with ui.element().classes('border-2 w-28 h-12 column items-center justify-center'):
                    ui.label(name)
            nd.note(f'{name}: {note}')
        with ui.row().classes('gap-1 mt-32'):
            giant('HTML', 'e.g. paragraphs, lists, tables')
            giant('CSS', 'e.g. shadows, transitions')
            giant('JavaScript', 'e.g. geolocation, third-party libraries')
            giant('Quasar', 'use even more components, dark mode')
            giant('Tailwind CSS', 'consistent and concise styling, responsive design')
            giant('Vue', 'NiceGUI: only 350 lines of own frontend code')
            giant('FastAPI', 'e.g. REST, authentication, existing backend')
            giant('Python', 'popular language with lots of features, many libraries and large community')
        nd.note('''
            - all these technologies at your fingertips
            - no need to learn them all, nicely abstracted away
        ''')

    with slide('To the Stars!'):
        with ui.column():
            ui.label('Version 1.0 is about to turn 1 year old 🎂')
            ui.label('Almost weekly releases 🚀')
            ui.markdown('''
                Active community on [GitHub](https://github.com/zauberzeug/nicegui/),
                [Discord](https://discord.com/invite/TEpFeAaF4f),
                [Reddit](https://www.reddit.com/r/nicegui/), and on
                [StackOverflow](https://stackoverflow.com/questions/tagged/nicegui).
            ''')
            ui.link('nicegui.io', 'https://nicegui.io')
            ui.link('zauberzeug.com', 'https://zauberzeug.com')
        nd.note('Meanwhile: JustPy discontinued')

ui.run(title='PyCon Ireland 2023',
       uvicorn_reload_includes='*.py, *.css')
