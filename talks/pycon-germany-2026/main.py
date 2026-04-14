#!/usr/bin/env python3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from pygments.formatters import HtmlFormatter
from pygments.styles.solarized import DARK_COLORS, LIGHT_COLORS, SolarizedDarkStyle, SolarizedLightStyle, make_style

import nicedeck as nd
from nicegui import ui
from windows import browser_window, code_window, demo


SNIPPETS = Path(__file__).parent / 'snippets'

TEXT_80 = 'text-black/80 dark:text-white/80'
TEXT_60 = 'text-black/60 dark:text-white/60'

_FACE_SVG = (Path(__file__).parent / 'assets' / 'happy_face.svg').read_text()


def setup():
    class SolarizedLight(SolarizedLightStyle):
        styles = make_style({**LIGHT_COLORS, 'base0': '#1a1d26', 'base01': '#4a4f5a'})

    class SolarizedDark(SolarizedDarkStyle):
        styles = make_style({**DARK_COLORS, 'base0': '#edeff3', 'base01': '#9ba2ae'})

    ui.add_css('.q-carousel__navigation-icon--active .q-icon {color:  #78909c !important; }')
    ui.add_css('''
        @keyframes nicegui-blink { 0%, 90%, 100% { transform: scaleY(1) } 95% { transform: scaleY(0.1) } }
        .svg_eye { animation: nicegui-blink 5s ease-in-out infinite; transform-box: fill-box; transform-origin: center }
    ''')
    ui.add_css(f'''
        {HtmlFormatter(nobackground=True, style=SolarizedLight).get_style_defs('div.codehilite')}
        {HtmlFormatter(nobackground=True, style=SolarizedDark).get_style_defs('.body--dark div.codehilite')}
    ''')


@contextmanager
def slide_layout(heading: str | None = None, *, center_heading: str | None = None) -> Generator[None, None, None]:
    if heading:
        nd.heading(heading)
    if center_heading:
        nd.center_heading(center_heading)
    with nd.center_row():
        yield


def insight(text: str) -> None:
    with nd.step():
        with ui.row(wrap=False, align_items='center') \
            .classes('absolute bottom-24 left-[50%] translate-x-[-50%] w-max text-lg pl-0 pr-5 py-0 gap-4 rounded-xl '
                     f'border border-blue-500/20 bg-blue-50 dark:bg-blue-950 {TEXT_80} shadow-lg overflow-hidden'):
            ui.icon('lightbulb', size='sm').classes('bg-blue-500 text-white/90 size-12')
            ui.markdown(text)


# --- 1. Title Slide ---
@nd.slide('''
    Hello everyone!

    Talk serves two purposes:

    1. show NiceGUI
    2. share general insights
''')
def _():
    ui.element().classes(
        'absolute inset-0 pointer-events-none '
        'bg-[radial-gradient(ellipse_at_50%_35%,color-mix(in_srgb,#5898d4_8%,transparent)_0%,transparent_60%)]'
    )
    with nd.center_row():
        with ui.column().classes('absolute-center items-center text-center gap-4'):
            ui.html(_FACE_SVG).classes('size-36 m-4')
            ui.markdown('# **5 Years of *NiceGUI***').classes('[&_em]:text-(--q-primary) [&_em]:not-italic')
            ui.label('What We Learned About Designing Pythonic UIs').classes(f'text-3xl {TEXT_80}')
            with ui.row(align_items='center').classes(f'mt-8 text-lg {TEXT_60}'):
                ui.label('Falko Schindler')
                ui.space().classes('w-8')
                ui.interactive_image('assets/zauberzeug-logo.webp').classes('h-8 dark:invert')
            with ui.row(align_items='center').classes(f'mt-2 text-lg {TEXT_60}'):
                ui.icon('language')
                ui.link('nicegui.io', 'https://nicegui.io').classes('text-current no-underline')
                ui.space().classes('w-8')
                ui.icon('commit')
                ui.link('github.com/zauberzeug/nicegui', 'https://github.com/zauberzeug/nicegui') \
                    .classes('text-current no-underline')


# --- 2. Who Am I ---
@nd.slide('''
    introduction

    *Zauberzeug* — "magic tools"

    *agricultural robots*, Feldfreund

    needed *dashboards for real hardware*

    5 years of development
''')
def _():
    with slide_layout():
        with ui.column().classes('gap-16 m-auto'):
            with ui.row(align_items='center'):
                ui.image('assets/falko.webp').classes('w-32 rounded-full')
                with ui.column().classes('gap-2'):
                    ui.label('Falko Schindler').classes(f'text-xl font-bold {TEXT_80}')
                    ui.link('github.com/falko-schindler', 'https://github.com/falko-schindler') \
                        .classes(f'text-lg {TEXT_60} no-underline')
            with ui.row(wrap=False).classes(f'text-lg {TEXT_60}'):
                with ui.column():
                    ui.interactive_image('assets/office.webp').classes('h-60 shadow')
                    with ui.row(align_items='center').classes('w-full'):
                        ui.label('Zauberzeug, Münster, Germany')
                with ui.column():
                    ui.interactive_image('assets/field-friend.webp').classes('h-60 shadow')
                    ui.label('Field Friend, our agricultural robot')


# --- 3. The Question: JustPy vs NiceGUI ---
@nd.slide('''
    question: which code preferred?

    ---

    both do the same

    why one feel nicer?

    7 insights about designing Pythonic APIs
''')
def _():
    with slide_layout('What Makes an API Feel Pythonic?'):
        with ui.grid(columns='1fr 1fr').classes('gap-x-8 gap-y-4 w-[95%]'):
            code_window(SNIPPETS / 'intro_justpy.py')
            with code_window('''
                from nicegui import ui

                with ui.card():
                    with ui.row():
                        ui.button('Click me') \\
                            .on_click(lambda: label.set_text('Hello PyCon! ❤️'))
                        label = ui.label('Hello Darmstadt!')

                ui.run()
            '''):
                with nd.step().classes(r'relative grow left-4 bottom-4 w-[calc(100%-2rem)]'):
                    @browser_window
                    def _():
                        with ui.card().classes('m-8'):
                            with ui.row():
                                ui.button('Click me') \
                                    .on_click(lambda: label.set_text('Hello PyCon! ❤️'))
                                label = ui.label('Hello Darmstadt!')


# --- 4. The Sweet Spot: Streamlit vs NiceGUI ---
@nd.slide('''
    JustPy: *low-level* end

    ---

    *Streamlit*: magically nice at first glance...

    if conditions...

    ---

    with state: too much magic

    ---

    We wanted *sweet spot*
    *high-level components*, *explicit state*, *real Python*.

    guided every API decision
''')
def _():
    with slide_layout('The Sweet Spot'):
        with ui.grid(columns='1fr 1fr 1fr').classes('gap-4 w-full items-start scale-95'):
            with ui.column().classes('gap-1'):
                ui.label('too low-level').classes(f'text-sm {TEXT_60}')
                code_window(SNIPPETS / 'intro_justpy.py')
            with nd.step(min=3), ui.column().classes('gap-1'):
                ui.label('sweet spot').classes(f'text-sm {TEXT_60}')
                code_window('''
                    from nicegui import ui

                    with ui.card():
                        with ui.row():
                            ui.button('Click me', on_click=lambda:
                                label.set_text('Hello PyCon! ❤️'))
                            label = ui.label('Hello Darmstadt!')

                    ui.run()
                ''').classes('border')
            with nd.step(min=1), ui.column().classes('gap-1'):
                ui.label('too much magic').classes(f'text-sm {TEXT_60}')
                code_window(SNIPPETS / 'simple_streamlit.py')
                with nd.step(min=2).classes('mt-6'):
                    code_window(SNIPPETS / 'intro_streamlit.py')


# --- 5. Context Managers Are the Layout API ---
@nd.slide('''
    UI has *hierarchy*

    *HTML*: tags

    *NiceGUI*: with statements

    "within"

    ---

    not just UI: any domain with hierarchy
''')
def _():
    with slide_layout('Context Managers Are the Layout API'):
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

        insight('The with statement is a "within" statement — code shape mirrors UI shape.')


# --- 6. Method Chaining as Progressive Disclosure ---
@nd.slide('''
    *UI* elements: *many options*

    parameters + methods → messy

    ---

    return *self*,
    *chain* them,
    *fluent API*,
    create and configure in *one statement*

    ---

    - *2 children*
    - *one thing* per line,
    - no name

    *progressive disclosure*

    lambdas...
''')
def _():
    with slide_layout('Method Chaining'):
        with ui.grid(columns='1fr 1fr').classes('gap-x-8 gap-y-4 w-[95%] items-start'):
            @demo(mode='rows')
            def _():
                with ui.card() as card:
                    card.classes('m-auto')
                    button = ui.button('Click me!', icon='face')
                    button.props('outline')
                    button.style('box-shadow: 0 0 1rem 0 rgba(0, 127, 255, 0.25)')
                    button.on('mouseenter', lambda e: e.sender.classes('scale-125'))
                    button.on('mouseleave', lambda e: e.sender.classes(remove='scale-125'))
                    ui.label('What a mess!')

            with nd.step():
                @demo(mode='rows')
                def _():
                    with ui.card().classes('m-auto'):
                        ui.button('Click me!', icon='face') \
                            .props('outline') \
                            .style('box-shadow: 0 0 1rem 0 rgba(0, 127, 255, 0.25)') \
                            .on('mouseenter', lambda e: e.sender.classes('scale-125')) \
                            .on('mouseleave', lambda e: e.sender.classes(remove='scale-125'))
                        ui.label('What a nice button!')

        insight('A fluent API lets you create and configure a UI element in one statement.')


# --- 7a. Lambdas & Callbacks ---
@nd.slide('''
    Left: classic, named functions

    works, lot of *ceremony*

    ---

    Right: *same behavior*, lambdas

    *cause and effect in one line*

    - `set_text`
    - optional event parameter
''')
def _():
    with slide_layout('Lambdas & Callbacks'):
        with ui.grid(columns='0.9fr 1fr').classes('gap-x-8 gap-y-4 w-[95%] items-start'):

            @demo(mode='rows')
            def _():
                from nicegui import events

                def handle_change(e: events.ValueChangeEventArguments) -> None:
                    ui.notify(f'New value: {e.value}')

                def handle_click() -> None:
                    label.text = 'Submitted 🚀'

                label = ui.label('Choose wisely:')
                ui.number(value=41, on_change=handle_change)
                ui.button('Submit', on_click=handle_click)

            with nd.step():
                @demo(mode='rows')
                def _():
                    label = ui.label('Choose wisely:')
                    ui.number(value=41, on_change=lambda e: ui.notify(f'New value: {e.value}'))
                    ui.button('Submit', on_click=lambda: label.set_text('Submitted 🚀'))


# --- 7b. Async / Await ---
@nd.slide('''
    *synchronous and asynchronous* handlers
''')
def _():
    with slide_layout('Async / Await'):

        @demo
        def _():
            import asyncio

            async def handle_click():
                ui.notify('Wait for it...')
                await asyncio.sleep(1)
                ui.notify('Click!')

            ui.button('Click me', on_click=handle_click)


# --- 7c. Auto-Context ---
@nd.slide('''
    something more subtle

    action in right context

    multiple clients

    ---

    callback as *lightweight* as the action
''')
def _():
    with slide_layout('Auto-Context'):

        @demo
        def _():
            with ui.row():
                with ui.card():
                    ui.button(icon='add', on_click=lambda: ui.label('Hello'))
                with ui.card():
                    ui.button(icon='add', on_click=lambda: ui.label('World'))

        insight('Callbacks should be as lightweight as the action they describe.')


# --- 8. Decorators Make Patterns Declarative ---
@nd.slide('''
    common pattern: clear + refill

    ---

    `@ui.refreshable`: *describe* the UI

    ---

    *same scaffolding* → decorator
''')
def _():
    with slide_layout('Decorators'):
        with ui.grid(columns='1fr 1fr').classes('gap-x-8 gap-y-4 w-[95%] items-start'):
            @demo(mode='rows')
            def _():
                def update():
                    container.clear()
                    with container:
                        if slider.value < 0:
                            ui.label(f'Freezing: {slider.value}°C').classes('text-blue')
                        elif slider.value < 10:
                            ui.label(f'Cold: {slider.value}°C').classes('text-green')
                        else:
                            ui.label(f'Warm: {slider.value}°C').classes('text-orange')

                slider = ui.slider(value=0, min=-10, max=20, on_change=update)
                container = ui.column()
                update()

            with nd.step():
                @demo(mode='rows')
                def _():
                    @ui.refreshable
                    def display():
                        if slider.value < 0:
                            ui.label(f'Freezing: {slider.value}°C').classes('text-blue')
                        elif slider.value < 10:
                            ui.label(f'Cold: {slider.value}°C').classes('text-green')
                        else:
                            ui.label(f'Warm: {slider.value}°C').classes('text-orange')

                    slider = ui.slider(value=0, min=-10, max=20, on_change=display.refresh)
                    display()

        insight('Decorators like `@ui.refreshable` eliminate our users\' boilerplate.')


# --- 9. Binding ---
@nd.slide('''
    another kind of repetition...

    some frameworks: special `State` containers/wrappers

    ---

    NiceGUI: *explicit* and *simple*

    strings suboptimal... yes, but
''')
def _():
    with slide_layout('Binding'):
        with ui.grid(rows='1fr 1fr').classes('gap-x-8 gap-y-4 w-[95%] items-start'):

            @demo
            def _():
                number = ui.number(value=42, on_change=lambda e: label.set_text(f'T = {e.value:.0f}°C'))
                label = ui.label(f'T = {number.value:.0f}°C')
                ui.slider(min=0, max=100, value=number.value, on_change=lambda e: number.set_value(e.value))

            with nd.step():
                @demo
                def _():
                    number = ui.number(value=42)
                    ui.label().bind_text_from(number, 'value', lambda v: f'T = {v:.0f}°C')
                    ui.slider(min=0, max=100).bind_value(number)


# --- 9b. Binding to Any Object ---
@nd.slide('''
    `@dataclass`

    ---

    *don't* force to restructure data models
''')
def _():
    with slide_layout('Binding'):

        @demo
        def _():
            from dataclasses import dataclass

            @dataclass
            class Temperature:
                value: float = 42

            temp = Temperature()

            ui.number().bind_value(temp, 'value')
            ui.label().bind_text_from(temp, 'value', lambda v: f'T = {v:.0f}°C')
            ui.slider(min=0, max=100).bind_value(temp, 'value')

        insight('Work with Python\'s object model, don\'t fight it.')


# --- 10. Design for the IDE ---
@nd.slide('''
    leaving runtime, *IDE experience*.

    [button coloring...]

    [API design ideas...]

    `DEFAULT_PROP`: *sentinel* with `__or__`, *`@resolve_defaults`*

    ---

    *best documentation*: one that the user never has to open
''')
def _():
    with slide_layout('Design for the IDE'):
        with ui.grid(columns='1fr 1fr').classes('gap-x-8 gap-y-4 w-[90%] items-start'):
            with ui.column().classes('gap-8'):
                with nd.step().classes('gap-1'):
                    ui.label('color = "primary"').classes(f'text-sm {TEXT_60}')
                    code_window('''
                        ui.button('Click me')
                    ''')
                with nd.step().classes('gap-1'):
                    ui.label('color = "red"').classes(f'text-sm {TEXT_60}')
                    code_window('''
                        ui.button('Click me', color='red')
                    ''')
                with nd.step().classes('gap-1'):
                    ui.label('color = "red"').classes(f'text-sm {TEXT_60}')
                    code_window('''
                        ui.button.default_props('color=red')
                        ui.button('Click me')
                    ''')
                with nd.step().classes('gap-1'):
                    ui.label('color = ?').classes(f'text-sm {TEXT_60}')
                    code_window('''
                        ui.button.default_props('color=red')
                        ui.button('Click me', color='primary')
                    ''')

            with ui.column():
                with nd.step():
                    code_window('''
                        class Button(...):
                            def __init__(self, ..., *, color: str = None, ...) -> None: ...
                    ''')
                with nd.step():
                    code_window('''
                        class Button(...):
                            def __init__(self, ..., *, color: str = DEFAULT, ...) -> None: ...
                    ''')
                with nd.step():
                    code_window('''
                        class Button(...):
                            @resolve_defaults
                            def __init__(self, ..., *, color: str = DEFAULT_PROP | 'primary', ...) -> None: ...
                    ''').classes('border')
                with nd.step():
                    ui.interactive_image('assets/button.png').classes('rounded shadow overflow-hidden')

        insight('Your best documentation is the one users never have to open.')


# --- 11. Escape Hatches ---
@nd.slide('''
    zoom out, *architecture*

    [NiceGUI stack]

    We don't *hide* the web.
    We make it *optional*.

    ---

    Users will *trust your abstractions* if they can *bypass them*.

    Always provide a *path to the layer below*.
''')
def _():
    with slide_layout('Escape Hatches'):
        def hatch(name: str, code: str) -> None:
            with ui.element().classes('row items-center text-xl'):
                ui.label(name).classes('text-lg w-28')
                with nd.step():
                    ui.code(code, language='python').classes('text-sm').copy_button.delete()

        with ui.card():
            ui.label('NiceGUI').classes('text-2xl')
            ui.separator()
            hatch('HTML', "ui.html('<div>Raw HTML</div>')")
            hatch('CSS', "label.style('color: red')")
            hatch('Tailwind', "label.classes('text-red')")
            hatch('Quasar', "button.props('outline')")
            hatch('JavaScript', "ui.run_javascript('alert(\"Hello\")')")
            hatch('FastAPI', "app.get('/hello')")
            hatch('Python', 'class MyCustomButton(ui.button): ...')

        insight('Always provide a path to the layer below.')


# --- 12. Beyond UI ---
@nd.slide('''
    step back: *7 insights*

    ---

    not just about UI, but *Python API design*
''')
def _():
    with slide_layout('Beyond UI'):
        groups = [
            ('Structure', [
                'Code shape should mirror domain shape',
                'Fluent APIs configure objects in one statement',
            ]),
            ('Events', [
                'Callbacks should be as lightweight as the action',
            ]),
            ('State', [
                'Turn repeated scaffolding into decorators',
                "Work with the language's object model",
            ]),
            ('Discoverability', [
                'Design for the IDE, not just runtime',
            ]),
            ('Trust', [
                'Always provide escape hatches',
            ]),
        ]
        with ui.column():
            with ui.grid(columns='auto 1fr').classes('gap-x-8 gap-y-2 text-xl items-baseline'):
                for i, (group, insights) in enumerate(groups):
                    if i > 0:
                        ui.separator().classes('col-span-2')
                    ui.label(group).classes(f'font-bold {TEXT_60}').style(f'grid-row: span {len(insights)}')
                    for insight_ in insights:
                        with nd.step():
                            ui.label(insight_)
            with nd.step():
                ui.markdown("_This isn't just about UI — it's about **Python API design**._") \
                    .classes(f'{TEXT_80} mt-8 text-xl')


# --- 13. Beyond Code ---
@nd.slide('''
    *culture*

    intentional pun: try to be *nice* to everyone and do things *right*.

    ---

    code review: simple solution wins

    ---

    docs: 100s live demos like in this talk

    ---

    GitHub: welcoming, answer with runnable snippets
''')
def _():
    with slide_layout('Beyond Code'):
        with ui.column().classes('items-center gap-8'):
            ui.label('NiceGUI = Nice Guy').classes('text-3xl')
            with ui.column().classes('items-center gap-4 text-xl'):
                with nd.step():
                    ui.label('Always strive for simple solutions — for users and developers alike')
                with nd.step():
                    ui.label('Build the NiceGUI website with NiceGUI')
                with nd.step():
                    ui.label('Foster a welcoming open-source culture on GitHub and beyond')


# --- 14. Thank You ---
@nd.slide('''
    *one final demo*

    quote from *Alan Kay* (object-oriented programming, personal computer)

    captures the essence of this talk

    ---

    "Simple things should be simple.
    Complex things should be possible."

    ---

    Thank you!

    find NiceGUI at *nicegui.io* and on *GitHub*

    Fun fact: like the website, this talk was built with NiceGUI!

    Now happy to take *questions*
''')
def _():
    with ui.column(align_items='center').classes('m-auto gap-16'):
        with ui.column(align_items='center').classes('gap-4'):

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

            with nd.step():
                ui.markdown('_"Simple things should be simple, complex things should be possible."_ — Alan Kay') \
                    .classes('text-xl')

        with nd.step().classes('items-center gap-8'):
            ui.label('Thank you!').classes('text-3xl font-medium')
            with ui.column(align_items='center').classes(f'gap-1 text-lg {TEXT_60}'):
                with ui.row(align_items='center'):
                    ui.icon('language')
                    ui.link('nicegui.io', 'https://nicegui.io').classes('text-current no-underline')
                with ui.row(align_items='center'):
                    ui.icon('commit')
                    ui.link('github.com/zauberzeug/nicegui', 'https://github.com/zauberzeug/nicegui') \
                        .classes('text-current no-underline')


nd.run(
    setup=setup,
    classes='bg-[#fafbfc] dark:bg-[#0f1117]',
    props='control-color=blue-grey-2',
    time_limit=30 * 60,
    title='PyCon Germany 2026',
    uvicorn_reload_includes='*.py, *.css',
    dark=None,
)
