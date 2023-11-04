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
        nd.heading('Three-line Hello World')
        with nd.center_row():
            with ui.column():
                with ui.row():
                    code = nd.code('''
                        from nicegui import ui

                        ui.label('Hello world!')

                        ui.run()
                    ''')
                    nd.code_result(code)
                ui.label('No command line tool to run, no build step, browser opens automatically.')
                ui.label('Easy for sharing code examples for documentation and Q&A.')

    with nd.slide():
        nd.heading('Hierarchical Layout')
        with nd.center_row():
            code = nd.code('''
                from nicegui import ui

                with ui.card():
                    with ui.row():
                        ui.label('Hello')
                        ui.label('world!')

                ui.run()
            ''')
            nd.code_result(code)

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
        with nd.center_row():
            code = nd.code('''
                from nicegui import ui
                        
                ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))
                        
                ui.run()
            ''')
            nd.code_result(code)

    with nd.slide():
        nd.heading('Event Handling: With/without Arguments')
        with nd.center_row():
            code = nd.code('''
                from nicegui import ui
                        
                ui.number(value=41, on_change=lambda e: ui.notify(f'new value: {e.value}'))
                        
                ui.run()
            ''')
            nd.code_result(code)

    with nd.slide():
        nd.heading('Event Handling: Auto-Context')
        with nd.center_row():
            code = nd.code('''
                from nicegui import ui
                        
                with ui.card():
                    ui.button('Spawn', on_click=lambda: ui.label("I'm here!"))

                ui.run()
            ''')
            nd.code_result(code)

    with nd.slide():
        nd.heading('Event Handling: Sync/Async')
        with nd.center_row():
            code = nd.code('''
                from nicegui import ui

                async def handle_click():
                    ui.notify('Clicked!')

                ui.button('Click me', on_click=handle_click)
                        
                ui.run()
            ''')
            nd.code_result(code)

    with nd.slide():
        nd.heading('Event Handling: Async Lambdas')
        with nd.center_row():
            code = nd.code('''
                from nicegui import ui

                async def notify(value):
                    ui.notify(f'New value: {value}')

                ui.number(value=12, on_change=lambda e: notify(e.value))
                        
                ui.run()
            ''')
            nd.code_result(code)

    with nd.slide():
        with ui.column().classes('absolute-center'):
            ui.markdown('''
                ### NiceGUI's Niceness
                
                - `with` contexts
                - event handler mit/ohne args, sync oder async, async lambdas, mit Kontext
                - builder pattern: `.style`, `.classes`, `.props`
                - CSS, Quasar, Tailwind
                - Tailwind API
                - lambda-friendly event registration
                - binding
                - `ui.refreshable`
                - `ui.markdown` with indented multiline string
            ''')

    with nd.slide():
        with ui.column().classes('absolute-center'):
            ui.markdown('### Applications')
            ui.link('zauberzeug.com', 'https://zauberzeug.com')
            ui.link('nicegui.io', 'https://nicegui.io')

ui.run(title='PyCon Ireland 2023')
