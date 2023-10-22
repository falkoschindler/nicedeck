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
        with ui.row().classes('absolute-center items-center'):
            code = nd.code('''
                from nicegui import app, ui

                ui.label('Hello World')

                ui.run()
            ''')
            with nd.step():
                nd.code_result(code)

    with nd.slide():
        with ui.row().classes('absolute-center items-center'):
            code = nd.code('''
                from nicegui import app, ui

                ui.button('Click me', on_click=lambda: ui.notify('Hello World'))

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
