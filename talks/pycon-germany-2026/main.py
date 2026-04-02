#!/usr/bin/env python3
from contextlib import contextmanager
from pathlib import Path
from pygments.formatters import HtmlFormatter
from pygments.styles.solarized import DARK_COLORS, LIGHT_COLORS, SolarizedDarkStyle, SolarizedLightStyle, make_style
from typing import Generator

import nicedeck as nd
from nicegui import ui
from windows import code_window, demo


SNIPPETS = Path(__file__).parent / 'snippets'


class SolarizedLight(SolarizedLightStyle):
    styles = make_style({**LIGHT_COLORS, 'base0': '#1a1d26', 'base01': '#4a4f5a'})


class SolarizedDark(SolarizedDarkStyle):
    styles = make_style({**DARK_COLORS, 'base0': '#edeff3', 'base01': '#9ba2ae'})


def root():
    @contextmanager
    def slide(heading: str | None = None, *,
              center_heading: str | None = None,
              hide_navigation: bool = False) -> Generator[None, None, None]:
        with nd.slide():
            if heading:
                nd.heading(heading)
            if center_heading:
                nd.center_heading(center_heading)
            if not hide_navigation:
                ui.label().bind_text_from(deck, 'value', lambda v: v.split('_')[-1]) \
                    .classes('absolute bottom-4 right-4 text-gray-400')
            with nd.center_row():
                yield

    ui.add_css('.q-carousel__navigation-icon--active .q-icon {color:  # 78909c !important; }')
    ui.add_css(f'''
        {HtmlFormatter(nobackground=True, style=SolarizedLight).get_style_defs('div.codehilite')}
        {HtmlFormatter(nobackground=True, style=SolarizedDark).get_style_defs('.body--dark div.codehilite')}
    ''')

    with nd.deck(time_limit=30 * 60).props('control-color=blue-grey-2').classes('bg-[#fafbfc] dark:bg-[#0f1117]') as deck:

        # --- 1. Title Slide ---
        with slide(hide_navigation=True):
            nd.note('''
                Who knows NiceGUI already?

                This talk: 5 years of building a Python UI framework.
                What Python language features make great UI APIs?
                Practical insights useful beyond NiceGUI.
            ''')
            with ui.column().classes('absolute-center items-center gap-4'):
                ui.markdown('# **5 Years of *NiceGUI***').classes('[&_em]:text-(--q-primary) [&_em]:not-italic')
                ui.label('What We Learned About Designing Pythonic UIs').classes('text-3xl text-gray-800')
                with ui.row().classes('gap-8 mt-8'):
                    ui.label('Falko Schindler').classes('text-lg text-gray-600')
                    ui.label('Zauberzeug').classes('text-lg text-gray-600')
                with ui.row().classes('gap-8 mt-2'):
                    ui.label('nicegui.io').classes('text-lg text-gray-400')
                    ui.label('github.com/zauberzeug/nicegui').classes('text-lg text-gray-400')

        # --- 2. The Question: JustPy vs NiceGUI ---
        with slide(heading='What Makes an API Feel Pythonic?'):
            nd.note('''
                Open cold. Start with code, not introduction.

                "Both do the same thing.
                One reads like a to-do list. The other reads like the UI it describes."

                "What's the difference? It's which Python features the designer chose to use."

                Some observations — the Zen of Python in action:
                - "Readability counts" — the code reads like the UI looks
                - "Beautiful is better than ugly" — indentation mirrors hierarchy
                - "Simple is better than complex" — 8 lines vs 22

                ---

                "We've been building NiceGUI for 5 years.
                Here's what we learned about letting Python do the design work."
                I'm Falko, Zauberzeug (robotics company near Münster), lead developer of NiceGUI.
            ''')
            with ui.grid(columns='auto auto').classes('gap-x-8 gap-y-4 w-[95%]'):
                code_window(SNIPPETS / 'intro_justpy.py')

                @demo(mode='rows')
                def _():
                    with ui.card():
                        with ui.row():
                            ui.button('Click me', on_click=lambda: label.set_text('Hello World!'))
                            label = ui.label('Hello Darmstadt!')

        # --- 3. The Sweet Spot: Streamlit vs NiceGUI ---
        with slide(heading='The Sweet Spot'):
            nd.note('''
                "That was the low-level end. Now the other extreme."

                Streamlit at its best — nothing beats this for a quick hello world.
                But: the "Hello World!" disappears on next interaction.

                ---

                Try the same persistent button interaction:
                session_state for a text change, st.rerun() to update,
                if st.button(...) — control flow as event handling.
                The framework decides when your code runs.

                ---

                "We wanted the sweet spot: high-level components, explicit state, real Python."
                Brief Zauberzeug context: we build robots — hardware, motors, cameras.
                We needed dashboards that work, not a thesis project on web frameworks.
                This constraint guided every API decision since.
            ''')
            with ui.grid(columns='auto auto').classes('gap-x-8 gap-y-4 w-[95%]'):
                code_window('''
                    import streamlit as st

                    st.write('Hello Darmstadt!')

                    if st.button('Click me'):
                        st.write('Hello World!')
                ''')
                with nd.step():
                    code_window(SNIPPETS / 'intro_streamlit.py')

        # --- TODO: remaining slides ---
        with slide(heading='Coming soon...'):
            ui.label('Coming soon...')


ui.run(root=root, title='PyCon Germany 2026', uvicorn_reload_includes='*.py, *.css')
