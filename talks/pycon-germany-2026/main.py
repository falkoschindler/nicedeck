#!/usr/bin/env python3
from contextlib import contextmanager
from typing import Generator

import nicedeck as nd
from nicegui import ui


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

    with nd.deck(time_limit=30 * 60) as deck:

        # --- 1. Title Slide ---
        with slide(hide_navigation=True):
            nd.note('''
                Who knows NiceGUI already?

                This talk: 5 years of building a Python UI framework.
                What Python language features make great UI APIs?
                Practical insights useful beyond NiceGUI.
            ''')
            with ui.column().classes('absolute-center items-center gap-4'):
                ui.markdown('*NiceGUI*').classes('text-5xl font-medium')
                ui.label('5 Years of NiceGUI').classes('text-4xl text-gray-800')
                ui.label('What We Learned About Designing Pythonic UIs').classes('text-2xl text-gray-600')
                with ui.row().classes('gap-8 mt-8'):
                    ui.label('Falko Schindler').classes('text-lg text-gray-600')
                    ui.label('Zauberzeug').classes('text-lg text-gray-600')
                with ui.row().classes('gap-8 mt-2'):
                    ui.label('nicegui.io').classes('text-lg text-gray-400')
                    ui.label('github.com/zauberzeug/nicegui').classes('text-lg text-gray-400')

        # --- 2. The Origin Story ---
        with slide(heading='The Origin Story'):
            nd.note('''
                Zauberzeug = "magic tools", robotics company near Münster.
                We build robots — hardware, electronics, software, AI.
                Needed UIs for motors, cameras, LEDs.

                ---

                Streamlit: too much magic — implicit reruns, hidden state.
                JustPy: too low-level — raw HTML elements.
                What if we build something in the middle?
            ''')
            with ui.column().classes('items-center gap-8'):
                with ui.row().classes('gap-16 items-center'):
                    with ui.column().classes('items-center'):
                        ui.label('Zauber').classes('font-bold text-2xl')
                        ui.label('[ˈtsaʊ̯bər]').classes('text-grey text-xs')
                        ui.label('"magic"')
                    with ui.column().classes('items-center'):
                        ui.label('zeug').classes('font-bold text-2xl')
                        ui.label('[ˈt͡sɔʏ̯k]').classes('text-grey text-xs')
                        ui.label('"tools"')
                with nd.step(), ui.row().classes('gap-8 text-xl'):
                    ui.label('Streamlit: too much magic')
                    ui.label('|').classes('text-gray-400')
                    ui.label('JustPy: too low-level')
                with nd.step():
                    ui.label('The Goldilocks moment: build something in the middle') \
                        .classes('text-xl text-primary')

        # --- 3. Three Lines to Delight ---
        with slide(heading='Three Lines to Delight'):
            nd.note('''
                Minimal NiceGUI app: 3 lines.
                Auto-opens browser, hot-reload, live web UI — zero config.
                Design principle: front-load delight, defer complexity.
            ''')

            @nd.demo
            def _():
                ui.label('Hello PyCon DE!')

        # --- 4. Context Managers for Composition ---
        with slide(heading='Context Managers'):
            nd.note('''
                "The shape of the code mirrors the hierarchy of the DOM."
                The `with` statement as a "within" statement.
                Indentation = nesting on screen.
            ''')

            @nd.demo
            def _():
                with ui.card():
                    with ui.row():
                        ui.label('Hello')
                        ui.label('world!')

        # --- 4b. Hierarchy Comparison ---
        with slide(heading='Hierarchy in Other Frameworks'):
            nd.note('''
                Compare how different frameworks express the same structure.
                HTML: explicit tags.
                NiceGUI: Python indentation mirrors the DOM.
                JustPy: imperative add() calls — structure not visible.
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
                ''')
            with nd.step():
                ui.label('JustPy').classes('text-2xl text-gray-600')
                nd.code('''
                    container = Div()
                    box = Div()
                    box.add(Div(text='Hello'))
                    box.add(Div(text='world!'))
                    container.add(box)
                ''')

        # --- 5. Method Chaining / Builder Pattern ---
        with slide(heading='Builder Pattern'):
            nd.note('''
                Fluent API: .classes(), .style(), .props(), .on()
                Style and events chained in a single statement.
                Progressive complexity without restructuring.
            ''')

            @nd.demo
            def _():
                ui.button('Nice!', icon='face') \
                    .props('outline') \
                    .classes('m-auto') \
                    .style('box-shadow: 0 0 1rem 0 rgba(0, 127, 255, 0.25)') \
                    .on('mouseenter', lambda e: e.sender.classes('scale-125')) \
                    .on('mouseleave', lambda e: e.sender.classes(remove='scale-125'))

        # --- 6. Lambdas & Callbacks ---
        with slide(heading='Lambdas & Callbacks'):
            nd.note('''
                on_click=lambda: ... — Pythonic, not framework-magic.
                With or without event arguments.
                Contrast with Streamlit's rerun model.
            ''')

            @nd.demo
            def _():
                ui.number(value=41, on_change=lambda e: ui.notify(f'New value: {e.value}'))

                ui.button('Submit', on_click=lambda: ui.notify('Done.', type='positive'))

        # --- 6b. Auto-Context ---
        with slide(heading='Auto-Context'):
            nd.note('''
                UI created in event handlers appears in the right place.
                NiceGUI tracks page, element, and slot context automatically.
            ''')

            @nd.demo
            def _():
                with ui.row():
                    with ui.card():
                        ui.button(icon='add', on_click=lambda: ui.label('Hello'))
                    with ui.card():
                        ui.button(icon='add', on_click=lambda: ui.label('World'))

        # --- 7. Async/Await ---
        with slide(heading='Async / Await'):
            nd.note('''
                Async handler? No problem — just Python's native async.
                No special API needed.
            ''')

            @nd.demo
            def _():
                import asyncio

                async def handle_click():
                    ui.notify('Wait for it...')
                    await asyncio.sleep(1)
                    ui.notify('Click!')

                ui.button('Click me', on_click=handle_click)

        # --- 8. Decorators for Routing & Reactivity ---
        with slide(heading='Decorators'):
            nd.note('''
                @ui.page — FastAPI-style routing, familiar to Python devs.
                @ui.refreshable — declarative UI updates.
                Common pattern: clear and refill a container. Decorator does it for you.
            ''')

            @nd.demo
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

        # --- 9. Type Hints for IDE Support ---
        with slide(heading='Type Hints & IDE Support'):
            nd.note('''
                Flat ui.* namespace — type ui. and discover everything.
                Type hints power auto-complete and inline docs.
                Generic element types for proper chaining return types.
                IDE as the primary discovery mechanism.
            ''')
            with ui.column().classes('items-center gap-8'):
                ui.label('Type ui. and discover ~100 elements').classes('text-2xl')
                nd.code('''
                    ui.button(...)
                    ui.card(...)
                    ui.input(...)
                    ui.label(...)
                    ui.slider(...)
                    ui.table(...)
                    # ...
                ''')

        # --- 10. Dataclasses & Binding ---
        with slide(heading='Binding'):
            nd.note('''
                bind_value() / bind_text_from() — connect UI to data models.
                Works with any object that has attributes.
                Two-way and one-way binding with transform functions.
            ''')

            @nd.demo
            def _():
                number = ui.number(value=42)

                ui.label().bind_text_from(number, 'value', lambda v: f'T = {v:.0f}°C')

                ui.slider(min=0, max=100).bind_value(number)

        # --- 11. Sentinel Patterns ---
        with slide(heading='Sentinel Patterns'):
            nd.note('''
                Optional parameters: distinguish "not provided" from None.
                Enables cleaner APIs: omit vs. explicitly set to None.
                Small detail, big impact on usability.
            ''')
            with ui.column().classes('items-center gap-4'):
                nd.code('''
                    UNSET = object()

                    def update(name: str = UNSET, age: int = UNSET):
                        if name is not UNSET:
                            ...  # caller explicitly provided name
                        if age is not UNSET:
                            ...  # caller explicitly provided age
                ''')

        # --- 12. Escape Hatches ---
        with slide(heading='Escape Hatches'):
            nd.note('''
                Users trust abstractions only if they can bypass them.
                Four layers: Python → Tailwind/UnoCSS → Quasar → raw HTML/JS.
                Standing on the shoulders of giants.
            ''')
            box_classes = 'w-full border border-gray-500/20 h-12 column items-center justify-center text-xl rounded bg-gray-500/5 shadow'
            with ui.grid(columns=8).classes('w-[90%] gap-2'):
                with ui.element().classes(f'{box_classes} col-span-8'):
                    ui.label('NiceGUI')
                with nd.step(), ui.element().classes(f'{box_classes} col-span-1'):
                    ui.label('HTML')
                with nd.step(), ui.element().classes(f'{box_classes} col-span-1'):
                    ui.label('CSS')
                with nd.step(), ui.element().classes(f'{box_classes} col-span-1'):
                    ui.label('JavaScript')
                with nd.step(), ui.element().classes(f'{box_classes} col-span-1'):
                    ui.label('Vue')
                with nd.step(), ui.element().classes(f'{box_classes} col-span-1'):
                    ui.label('Quasar')
                with nd.step(), ui.element().classes(f'{box_classes} col-span-1'):
                    ui.label('Tailwind')
                with nd.step(), ui.element().classes(f'{box_classes} col-span-1'):
                    ui.label('FastAPI')
                with nd.step(), ui.element().classes(f'{box_classes} col-span-1'):
                    ui.label('Python')

        # --- 13. Beyond API: What Makes It "Nice" ---
        with slide(heading='What Makes It "Nice"'):
            nd.note('''
                The pun: NiceGUI = Nice Guy — "tries to be nice to everyone."
                "Prefer simple solutions" — a code review blocker, not a platitude.
                Dogfooding: nicegui.io is built with NiceGUI.
                Community: respond with code, not just words.
            ''')
            with ui.column().classes('items-center gap-8'):
                ui.label('NiceGUI = Nice Guy').classes('text-3xl')
                with nd.step(), ui.column().classes('items-center gap-4'):
                    ui.label('"Prefer simple solutions" — enforced, not aspirational').classes('text-xl')
                    ui.label('nicegui.io is built with NiceGUI').classes('text-xl')
                    ui.label('Respond with code, not just words').classes('text-xl')
                with nd.step(), ui.column().classes('items-center gap-2 text-lg'):
                    ui.label('5 years • 15k+ stars • ~100 elements • weekly releases')

        # --- 14. Takeaways ---
        with slide(heading='Takeaways'):
            nd.note('''
                Python's language features aren't just convenient — they're API design tools.
                The Goldilocks principle: not too much magic, not too low-level.
                DX is a consequence of caring about the same things your users care about.
            ''')
            with ui.column().classes('items-center gap-8 text-xl'):
                ui.label('Python features are API design tools')
                with nd.step():
                    ui.label('Context managers, decorators, lambdas, async, type hints')
                with nd.step():
                    ui.label('The Goldilocks principle: not too much magic, not too low-level')
                with nd.step():
                    ui.markdown('_"Developer experience is a consequence of caring about '
                                'the same things your users care about."_')

        # --- 15. Thank You ---
        with slide(hide_navigation=True):
            nd.note('''
                Thank you! Questions?
            ''')

            @nd.demo
            def _():
                ui.label('Thank you.') \
                    .classes('text-4xl text-primary')


ui.run(root=root, title='PyCon Germany 2026', uvicorn_reload_includes='*.py, *.css')
