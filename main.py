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
        else:
            ui.label().bind_text_from(deck, 'value', lambda v: v.split('_')[-1]) \
                .classes('absolute bottom-4 right-4 text-gray-400')
        with nd.center_row():
            yield


with nd.deck(time_limit=30 * 60) as deck:
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
                    ui.image('assets/favicon.png').classes('opacity-70 w-6')
                    ui.label('nicegui.io').classes('text-lg text-gray-600')
                with ui.row().classes('gap-2 items-center'):
                    ui.html((Path(__file__).parent / 'assets' / 'github.svg').read_text()).classes('opacity-70')
                    ui.label('github.com/zauberzeug/nicegui').classes('text-lg text-gray-600')

    with slide():
        nd.note('''
            - Zauberzeug, Münsterland, ~20 employees
            
            ---
            
            - hardware+software, **idea -> product**
            - electronics, mechanics, 3D printing, microcontrollers, software, and AI
            
            ---
            
            - 3 examples
            - **mobile** robots: out in the wild
        ''')
        with nd.heading():
            ui.image('assets/zauberzeug-logo.webp').classes('w-40')
        ui.image('assets/building.webp').classes('absolute w-full z-[-1] top-28 bottom-0')
        with nd.step(), nd.center_row():
            ui.image('assets/office.jpg').classes('absolute w-full z-[-1] top-28 bottom-0')
        with nd.center_row():
            with nd.step(), ui.card():
                ui.image('assets/brushing-bot.webp').classes('w-60 h-40 bg-white')
            with nd.step(), ui.card():
                ui.image('assets/robot-brain.webp').classes('w-60 h-40 bg-white')
            with nd.step(), ui.card():
                ui.image('assets/field-friend.webp').classes('w-60 h-40 bg-white')

    with slide('Philosophy'):
        nd.note('''
            - creating tools that feel like **magic**
            - quote
            - applies to software _and_ hardware
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
            - **Why?**
        ''')

    with slide('ODrive Motor Controller'):
        nd.note('''
            - mobile robots: motors
            - ODrive motor controller needs configuration and tuning
            - **Python** CLI, poor GUI
            - network!
            - perfect match: Streamlit?
        ''')
        ui.image('assets/odrive.jpg').classes('w-[30%]').props('fit=contain')
        with nd.step().classes('w-[60%]'):
            ui.image('assets/odrive-gui.png').props('fit=contain').classes('border shadow')

    with slide('Streamlit'):
        nd.note('''
            - UI framework for Python
            - popular for its simplicity
            - problems:
                - non-Pythonic syntax
                - constant reload
                - hard to manage state
                - hard to create something like timers
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

    with slide('Wishful Programming'):
        nd.note('''
            - what do we want?
            - working prototype after a few hours
            - FastAPI app + Angular
            - name? "Just Python"?
        ''')
        nd.code('''
            import simple_ui as ui

            ui.Label('Hello world!')
            ui.Button('Click me!', on_click=lambda: print('CLICK'))

            with ui.Row():
                ui.Checkbox('Option 1', on_change=lambda value: print('Option 1:', value))
                ui.Switch('Option 2', on_change=lambda value: print('Option 2:', value))

            with ui.Column():
                ui.TextInput(placeholder='Text')
                ui.NumberInput(value=1.0)

            ui.Radio(['A', 'B', 'C'], on_change=lambda value: print(value))
            ui.Select(['D', 'E', 'F'], on_change=lambda value: print(value))

            ui.run()
        ''')

    with slide('JustPy'):
        nd.note('''
            - Vue, Quasar, Tailwind
            - basis for 0.x
            - removed in 1.0
                - code base in poor condition
                - deprecated Vue and Quasar versions
                - too much overhead
        ''')
        nd.code('''
            import justpy as jp

            def hello_world_readme():
                wp = jp.WebPage()
                d = jp.Div(text='Hello world!')
                wp.add(d)
                return wp

            jp.justpy(hello_world_readme)
        ''')
        with nd.step():
            nd.code('''
                import justpy as jp

                def my_click(self, msg):
                    self.text = 'I was clicked!'

                def hello_world_readme2():
                    wp = jp.WebPage()
                    d = jp.Div(text='Hello world!')
                    d.on('click', my_click)
                    wp.add(d)
                    return wp

                jp.justpy(hello_world_readme2)
            ''')

    with slide('NiceGUI'):
        nd.note('''
            - "NiceGUI", pun intended
            - should be "nice" to use
            - Nice guy:
                "a man who puts the needs of others before his own,
                avoids confrontations,
                does favors,
                provides emotional support,
                tries to stay out of trouble,
                and generally acts nicely towards others"
                [wiki]
            
            ---
            
            - 3 lines
            - no build, CLI, or config files
            - browser opens
            - auto-reload
        ''')
        ui.image('assets/face.png').classes('w-40 mr-8')
        with nd.step().classes('self-center'), ui.row().classes('items-stretch'):
            @nd.demo
            def demo():
                ui.label('Hello world!')

    with slide('Embrace Indentation'):
        nd.note('''
            - Pythonic hierarchy? Indentation!
        ''')

        @nd.demo
        def demo():
            with ui.card():
                with ui.row():
                    ui.label('Hello')
                    ui.label('world!')

    with slide('Hierarchy in Other UI Frameworks'):
        nd.note('''
            ...
        ''')
        with nd.step(0):
            ui.label('HTML').classes('text-2xl text-gray-600')
            nd.code('''
                <div class="card">
                    <div class="row">
                        <span>Hello</span>
                        <span>world!</span>
                    </div>
                </div>
            ''', language='html')
        with nd.step():
            ui.label('NiceGUI').classes('text-2xl text-gray-600')
            nd.code('''
                with ui.card():
                    with ui.row():
                        ui.label('Hello')
                        ui.label('world!')
            ''').classes('flex-grow')
        with nd.step():
            ui.label('JustPy').classes('text-2xl text-gray-600')
            nd.code('''
                container = Div()
                box = Div()
                box.add(Div(text='Hello'))
                box.add(Div(text='world!'))
                container.add(box)
            ''').classes('flex-grow')

    with slide('Event Handling: Embrace Lambdas'):
        nd.note('''
            - "normal" event handling: callback functions
              (in contrast to Streamlit)
            
            - yes: this is live, slides written in NiceGUI!
        ''')

        @nd.demo
        def demo():
            ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))

    with slide('Behind the Scenes'):
        nd.note('''
            ...
        ''')
        with ui.column().classes('w-[30rem] items-stretch'):
            ui.chat_message('I\'d like to see "/".', avatar='assets/chrome.svg', sent=True)
            with nd.step().classes('items-stretch'):
                ui.chat_message('Here you go:\n<html>...<button />...<script />...</html>', avatar='assets/python.svg')
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
        nd.note('''
            - **some small conveniences**
        ''')

        @nd.demo
        def demo():
            ui.number(value=41, on_change=lambda e: ui.notify(f'new value: {e.value}'))

    with slide('Event Handling: Auto-Context'):
        nd.note('''
            - page, element, and slot
        ''')

        @nd.demo
        def demo():
            with ui.row():
                with ui.card():
                    ui.button(icon='add', on_click=lambda: ui.label('🙂'))
                with ui.card():
                    ui.button(icon='add', on_click=lambda: ui.label('😎'))

    with slide('Event Handling: Sync/Async'):
        nd.note('''
            - Your event handler is async? No problem!
        ''')

        @nd.demo
        def demo():
            import asyncio

            async def handle_click():
                ui.notify('Wait for it...')
                await asyncio.sleep(1)
                ui.notify('Click!')

            ui.button('Click me', on_click=handle_click)

    with slide('Event Handling: Async Lambdas'):
        nd.note('''
            - "async lambdas"
        ''')

        @nd.demo
        def demo():
            import asyncio

            async def notify(value):
                ui.notify('You chose...')
                await asyncio.sleep(1)
                ui.notify(value)

            ui.toggle(['A', 'B', 'C'], on_change=lambda e: notify(e.value))

    with slide('Builder Pattern'):
        nd.note('''
            - important concept: builder pattern
            - style and events chained in a single statement
        ''')

        @nd.demo
        def demo():
            ui.button('Nice!', icon='face') \
                .props('outline') \
                .classes('m-auto') \
                .style('box-shadow: 0 0 1rem 0 rgba(0, 127, 255, 0.25)') \
                .on('mouseenter', lambda e: e.sender.classes('scale-125')) \
                .on('mouseleave', lambda e: e.sender.classes(remove='scale-125'))

    with slide('Tailwind API'):
        nd.note('''
            - can use Tailwind API instead
        ''')

        @nd.demo
        def demo():
            ui.label('Tailwind CSS') \
                .tailwind \
                .text_color('blue-600') \
                .border_width('4') \
                .border_style('dashed') \
                .border_color('blue-600') \
                .padding('p-4')

    with slide('Binding'):
        nd.note('''
            - connect UI elements to each other and to data models
        ''')

        @nd.demo
        def demo():
            number = ui.number(value=42)

            ui.label().bind_text_from(number, 'value', lambda v: f'T = {v:.0f}˚C')

            ui.slider(min=0, max=100).bind_value(number)

    with slide('Refreshable UI'):
        nd.note('''
            - common pattern emerged: clear and refill container
            - introduced `refreshable` decorator
            - sync/async, w/wo arguments
        ''')

        @nd.demo
        def demo():
            @ui.refreshable
            def show_temperature():
                if slider.value < 0:
                    ui.label(f'Freezing: {slider.value}°C').classes('text-blue')
                elif slider.value < 10:
                    ui.label(f'Cold: {slider.value}°C').classes('text-green')
                else:
                    ui.label(f'Warm: {slider.value}°C').classes('text-orange')

            slider = ui.slider(value=0, min=-10, max=20, on_change=show_temperature.refresh)
            show_temperature()

    with slide('Refreshable UI with UI State'):
        nd.note('''
            - community: borrow React's state concept
        ''')

        @nd.demo
        def demo():
            @ui.refreshable
            def show_counter():
                count, set_count = ui.state(0)
                ui.label(f'Counter: {count}')
                ui.button('Increment', on_click=lambda: set_count(count + 1))

            show_counter()

    with slide('HTML, Markdown and More'):
        nd.note('''
            - use existing technologies
        ''')

        @nd.demo
        def demo():
            ui.html('''
                <p>This is <strong>HTML</strong>.</p>
            ''')
            ui.markdown('''
                This is **Markdown**.
            ''')
            ui.mermaid('''
                graph LR
                    This --> is --> Mermaid
            ''')
            ui.code('''
                import this
                
                print('This is Python')
            ''')

    with slide('On the Shoulders of Giants'):
        nd.note('''
            - NiceGUI is built on top of many great technologies
            - beginner-friendly abstraction
            - _can_ go deeper
            
            ---
        ''')

        def giant(name: str, note: str) -> ui.element:
            with nd.step().classes('border-2 h-12 column items-center justify-center'):
                ui.label(name)
            return f'**{name}**: {note}<br />'
        with ui.grid(columns=8).classes('mt-24 w-[90%] gap-1'):
            with ui.element().classes('border-2 h-12 column items-center justify-center col-span-8'):
                ui.label('NiceGUI')
            notes = ''
            notes += giant('HTML', 'e.g. paragraphs, lists, tables')
            notes += giant('CSS', 'e.g. shadows, transitions')
            notes += giant('JavaScript', 'e.g. geolocation, libraries')
            notes += giant('Quasar', 'dozens of components, even without NiceGUI integration')
            notes += giant('Tailwind CSS', 'consistent and concise styling, responsive design')
            notes += giant('Vue', 'heavy lifting on frontend')
            notes += giant('FastAPI', 'e.g. REST, authentication, existing backend')
            notes += giant('Python', 'popular language, libraries, community')
            nd.note(notes)

    with slide('Where are we at?'):
        nd.note('''
            ...
                
            - one of the most popular Python UI frameworks
            - 100s of open source projects build on top of NiceGUI
            - **RoSys**: UI and robot control in Python
            - JustPy discontinued
        ''')
        with ui.column().classes('self-center'):
            ui.label('Version 1.0 is about to turn 1 year old 🎂')
            ui.label('Around 100 UI elements 🧱')
            ui.label('Almost weekly releases 🚀')
            ui.label('Strong community 💪')
        with nd.step().classes('w-[20%]'), ui.column().classes('w-full'):
            ui.image('assets/github.jpg').classes('h-6').props('fit=contain')
            ui.image('assets/reddit.png').classes('h-6').props('fit=contain')
            ui.image('assets/discord.png').classes('h-6').props('fit=contain')
            ui.image('assets/stackoverflow.png').classes('h-6').props('fit=contain')
            ui.image('assets/chatgpt.png').classes('h-6').props('fit=contain')
        with nd.step(), nd.center_row().classes('absolute-center pb-[1%] pr-[2%]'):
            ui.image('assets/web-index.png').classes('w-[60%]')
        with nd.step(), nd.center_row().classes('absolute-center pt-[1%] pl-[2%]'):
            ui.image('assets/web-documentation.png').classes('w-[60%]')

    with slide('To the Stars!'):
        nd.note('''
            - robot on local network
        ''')

        with ui.column():
            with ui.row().classes('items-stretch'):
                @nd.demo
                def demo():
                    # import robot

                    ui.button('Start!', icon='smart_toy', on_click=lambda: robot.start())

            with nd.step().classes('w-full'):
                nd.code('''
                    $ python3 main.py
                    NiceGUI ready to go on http://localhost:8080, and http://192.168.0.209:8080
                ''', language=None).classes('bg-white h-32 w-full')

    with slide('To the Stars!'):
        nd.note('''
            - robot somewhere else
            - proxy server for remote access
            - send link to colleagues or friends!
        ''')
        with ui.row().classes('absolute-center -mt-48 gap-2'):
            ui.label('NiceGUI').classes('text-2xl font-bold')
            ui.label('On Air').classes('text-2xl font-bold text-primary')

        with ui.column():
            with ui.row().classes('items-stretch'):
                @nd.demo
                def demo():
                    # import robot

                    ui.button('Start!', icon='smart_toy', on_click=lambda: robot.start())

                    # ui.run(on_air=True)

            with nd.step().classes('w-full'):
                nd.code('''
                    $ python3 main.py
                    NiceGUI ready to go on http://localhost:1234, and http://192.168.0.209:1234
                    NiceGUI is on air at http://on-air.nicegui.io/devices/0gGsMGIS/
                ''', language=None).classes('bg-white h-32 w-full')

    with slide():
        nd.note('''
            - This brings me to the end of my talk.
            - I thank you for your attention
            - and I'm happy to answer your questions.
        ''')

        @nd.demo
        def demo():
            ui.label('Thank you.') \
                .classes('text-4xl text-primary')


ui.run(title='PyCon Ireland 2023',
       uvicorn_reload_includes='*.py, *.css')
