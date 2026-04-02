#!/usr/bin/env python3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from pygments.formatters import HtmlFormatter
from pygments.styles.solarized import DARK_COLORS, LIGHT_COLORS, SolarizedDarkStyle, SolarizedLightStyle, make_style

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

        # --- 4. Context Managers Are the Layout API ---
        with slide(heading='Context Managers Are the Layout API'):
            nd.note('''
                You already saw this — Python's indentation *is* the hierarchy.

                "The `with` statement is really a 'within' statement."

                HTML has the same nesting — hierarchy *should* be visible in code.
                JustPy lost it, NiceGUI got it back.

                ---

                **Lesson:** if your domain has hierarchy, Python already has the syntax for it.
                File systems, config trees, document structures — `with` blocks work everywhere.
            ''')
            with ui.grid(columns='1fr 1fr').classes('gap-x-8 gap-y-4 w-[95%] items-start'):
                code_window('''
                    <div class="card">
                        <div class="row">
                            <span>Hello</span>
                            <span>world!</span>
                        </div>
                    </div>
                ''', language='html')

                @demo(mode='rows')
                def _():
                    with ui.card():
                        with ui.row():
                            ui.label('Hello')
                            ui.label('world!')

        # --- 5. Method Chaining as Progressive Disclosure ---
        with slide(heading='Method Chaining'):
            nd.note('''
                A ui.button('Click') is nice and simple.
                But then you need styling. Then behavior.
                Do you need a completely different API now?

                No. You chain. Each method returns self — the builder pattern.
                Beginners never see .props() until they need it.

                Four layers of depth:
                Pure Python → Tailwind/UnoCSS → Quasar props → raw HTML/JS.
                You go deeper only when you choose to.

                ---

                **Lesson:** builder patterns let users add complexity without restructuring code.
                Beginners see simplicity, experts find power — without a mode switch.
            ''')

            @demo
            def _():
                ui.button('Nice!', icon='face') \
                    .props('outline') \
                    .classes('m-auto') \
                    .style('box-shadow: 0 0 1rem 0 rgba(0, 127, 255, 0.25)') \
                    .on('mouseenter', lambda e: e.sender.classes('scale-125')) \
                    .on('mouseleave', lambda e: e.sender.classes(remove='scale-125'))

        # --- 6. Lambdas Make Events Obvious ---
        with slide(heading='Lambdas & Callbacks'):
            nd.note('''
                Remember the `if st.button(...)` pattern?
                NiceGUI's answer: cause and effect in one line.

                With or without event argument —
                NiceGUI inspects the signature and does the right thing.

                ---

                **Lesson:** callbacks should be as lightweight as the action they describe.
                If your event handling requires more ceremony than the event itself, something is wrong.
            ''')

            @demo
            def _():
                ui.number(value=41, on_change=lambda e: ui.notify(f'New value: {e.value}'))

                ui.button('Submit', on_click=lambda: ui.notify('Done.', type='positive'))

        # --- 6b. Auto-Context ---
        with slide(heading='Auto-Context'):
            nd.note('''
                UI created in event handlers appears in the right place.
                NiceGUI tracks page, element, and slot context automatically.

                Click the left button → label appears in the left card.
                No explicit parent tracking.

                Context means more than just the container — it also tracks the *client*.
                Multiple users visit the same app → each user's events affect only their own UI.
                NiceGUI is a web framework after all.
            ''')

            @demo
            def _():
                with ui.row():
                    with ui.card():
                        ui.button(icon='add', on_click=lambda: ui.label('Hello'))
                    with ui.card():
                        ui.button(icon='add', on_click=lambda: ui.label('World'))

        # --- 7. Async/Await Just Works ---
        with slide(heading='Async / Await'):
            nd.note('''
                Handler needs to do something slow — API call, animation, delay.
                Just make it async.

                No special framework API. No run_in_executor. No callback pyramids.
                If Python's async/await works, your framework should accept it.

                ---

                **Lesson:** don't invent concurrency models when Python already has one.
            ''')

            @demo
            def _():
                import asyncio

                async def handle_click():
                    ui.notify('Wait for it...')
                    await asyncio.sleep(1)
                    ui.notify('Click!')

                ui.button('Click me', on_click=handle_click)

        # --- 8. Decorators Make Patterns Declarative ---
        with slide(heading='Decorators'):
            nd.note('''
                **Routing:** @ui.page('/settings') — if you know FastAPI, you already know this.
                Familiar patterns reduce learning curves.

                **Reactivity:** common pattern — clear a container, rebuild its contents.
                Tedious and error-prone.
                @ui.refreshable makes it declarative.
                The decorator handles clearing and rebuilding.
                You just describe what the UI should look like.

                ---

                **Lesson:** decorators turn recurring patterns into declarations.
                If you find yourself writing the same scaffolding around different logic,
                that's a decorator waiting to happen.
            ''')

            @demo
            def _():
                @ui.refreshable
                def show_temperature():
                    if slider.value < 0:
                        ui.label(f'Freezing: {slider.value}°C').classes('text-blue')
                    elif slider.value < 10:
                        ui.label(f'Cold: {slider.value}°C').classes('text-green')
                    else:
                        ui.label(f'Warm: {slider.value}°C').classes('text-orange')

                slider = ui.slider(value=0, min=-10, max=20,
                                   on_change=show_temperature.refresh)
                show_temperature()

        # --- 9. Design for the IDE ---
        with slide(heading='Design for the IDE'):
            nd.note('''
                Your API should be readable *before* the user runs it —
                in the IDE, in the tooltip, in the auto-complete dropdown.

                **Flat namespace:** ui.input, not ui.elements.input.TextInput.
                Type ui. and browse everything.

                **Type hints for chaining:** ui.button().classes() returns Button, not Element.

                **Explicit signatures over **kwargs:** JustPy passes everything as **kwargs —
                the IDE can't help you. NiceGUI spells out every parameter.

                **Honest defaults:** DEFAULT_PROP is a sentinel with __or__ overloaded
                so the | 'primary' shows up in the signature.
                @resolve_defaults does the actual resolution at call time.
                A bit of magic — but in service of a crystal-clear API surface.

                "Your best documentation is the one the user never has to open."

                ---

                **Lesson:** every design choice should survive the IDE test —
                does auto-complete, the tooltip, the signature tell the user what they need?
            ''')
            with ui.column().classes('gap-4 w-[95%]'):
                with ui.row().classes('gap-8 text-xl'):
                    ui.label('ui.input').classes('font-mono')
                    ui.label('not').classes('text-gray-400')
                    ui.label('ui.elements.input.TextInput').classes('font-mono line-through text-gray-400')
                with nd.step():
                    code_window('''
                        class Button(...):
                            @resolve_defaults
                            def __init__(
                                self,
                                text: str = '', *,
                                on_click: Handler[ClickEventArguments] | None = None,
                                color: str | None = DEFAULT_PROP | 'primary',
                                icon: str | None = DEFAULT_PROP | None,
                            ) -> None:
                    ''')

        # --- 10. Binding Leverages Python's Object Model ---
        with slide(heading='Binding'):
            nd.note('''
                UI shows data. Data changes. UI must update.
                Classic two-way sync nightmare.

                Some frameworks: inherit from Observable, use special State containers.
                (Looking at you, Reflex.)

                We actually tried the magical version first: car.driver.bind(person.name) —
                using monkey-patching and caller introspection.
                (See github.com/zauberzeug/binding.)
                Beautiful syntax, but too fragile for a mature library.

                NiceGUI's approach is explicit: pass the object and attribute name as strings.
                Works with any object that has attributes — dataclasses, plain classes, other UI elements.
                No base class required. No registration. Just Python objects.

                ---

                **Lesson:** don't force users to restructure their data model for your framework.
                Work with what Python already gives you.
            ''')

            @demo
            def _():
                number = ui.number(value=42)

                ui.label().bind_text_from(number, 'value', lambda v: f'T = {v:.0f}°C')

                ui.slider(min=0, max=100).bind_value(number)

        # --- 11. Escape Hatches ---
        with slide(heading='Escape Hatches'):
            nd.note('''
                "Every layer here is something you can reach into directly."

                .classes('...') → Tailwind.
                .props('...') → Quasar.
                ui.html() → raw HTML.
                ui.run_javascript() → raw JS.
                app.routes → full FastAPI.

                "We don't hide the web. We make it optional."
                "Users trust your abstractions only if they know they can bypass them."

                ---

                **Lesson:** always provide a path to the layer below.
                The moment users feel trapped, they leave.
            ''')
            box = 'w-full border border-gray-500/20 h-12 column items-center justify-center text-xl rounded bg-gray-500/5 shadow'
            with ui.grid(columns=8).classes('w-[90%] gap-2'):
                with ui.element().classes(f'{box} col-span-8'):
                    ui.label('NiceGUI')
                with nd.step(), ui.element().classes(box):
                    ui.label('HTML')
                with nd.step(), ui.element().classes(box):
                    ui.label('CSS')
                with nd.step(), ui.element().classes(box):
                    ui.label('JavaScript')
                with nd.step(), ui.element().classes(box):
                    ui.label('Vue')
                with nd.step(), ui.element().classes(box):
                    ui.label('Quasar')
                with nd.step(), ui.element().classes(box):
                    ui.label('Tailwind')
                with nd.step(), ui.element().classes(box):
                    ui.label('FastAPI')
                with nd.step(), ui.element().classes(box):
                    ui.label('Python')

        # --- 12. Beyond API: What Makes It "Nice" ---
        with slide(heading='What Makes It "Nice"'):
            nd.note('''
                The name: NiceGUI = Nice Guy —
                "a guy who tries to be nice to everyone and do things right."

                "Prefer simple solutions" — this is in our code review rules as a **blocker**.
                Not a guideline.
                If a simpler design meets the requirements, the complex one is rejected.

                Dogfooding: nicegui.io — the entire website, docs, live demos —
                is built with NiceGUI. We find our own bugs before users do.

                Community: when someone asks a question, we reply with a working code snippet.
                Helpfulness is measured in runnable examples.
            ''')
            with ui.column().classes('items-center gap-8'):
                ui.label('NiceGUI = Nice Guy').classes('text-3xl')
                with nd.step(), ui.column().classes('items-center gap-4 text-xl'):
                    ui.label('"Prefer simple solutions" — enforced, not aspirational')
                    ui.label('nicegui.io is built with NiceGUI')
                    ui.label('Respond with code, not just words')
                with nd.step():
                    ui.label('5 years \u2022 15k+ stars \u2022 ~120 elements \u2022 frequent releases') \
                        .classes('text-lg')

        # --- 13. Takeaways ---
        with slide(heading='Takeaways'):
            nd.note('''
                No new information — just crystallize.

                Python's language features are API design tools.
                Context managers, decorators, lambdas, async, type hints, the object model —
                use them deliberately, not accidentally.

                Find the sweet spot. Not too much magic, not too low-level.
                The right abstraction lets users think in their domain, not yours.

                These lessons aren't about UI.
                CLI tools, ORMs, data pipelines, testing frameworks —
                any Python API benefits from the same thinking.
            ''')
            with ui.column().classes('items-center gap-8 text-xl'):
                ui.label('Python features are API design tools')
                with nd.step():
                    ui.label('Context managers, decorators, lambdas, async, type hints')
                with nd.step():
                    ui.label('Not too much magic, not too low-level')
                with nd.step():
                    ui.label('These lessons apply beyond UI: CLIs, ORMs, data pipelines, ...').classes('text-gray-600')
                with nd.step():
                    ui.markdown('_"Simple things should be simple, complex things should be possible."_ — Alan Kay')

        # --- 14. Thank You ---
        with slide(hide_navigation=True):
            nd.note('''
                Thank you! Questions?

                "Simple things should be simple. Complex things should be possible."
                This is both — a 3D scene in a few lines of Python.
            ''')

            @demo
            def _():
                from time import time
                import numpy as np

                def generate_data():
                    u, v = np.meshgrid(np.linspace(0, 1), np.linspace(0, 1))
                    w = np.sin(5 * u + time()) * np.cos(5 * v + time())
                    rgb = np.dstack([u, v, w / 2 + 0.5]).reshape(-1, 3)
                    return rgb * [6, 6, 2] - [3.5, 2, 0], rgb

                with ui.scene(grid=False, background_color='white'):
                    wave = ui.scene.point_cloud([], point_size=0.1)

                ui.timer(0.05, lambda: wave.set_points(*generate_data()))


ui.run(root=root, title='PyCon Germany 2026', uvicorn_reload_includes='*.py, *.css')
