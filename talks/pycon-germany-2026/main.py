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

TEXT_80 = 'text-black/80 dark:text-white/80'
TEXT_60 = 'text-black/60 dark:text-white/60'


def setup():
    class SolarizedLight(SolarizedLightStyle):
        styles = make_style({**LIGHT_COLORS, 'base0': '#1a1d26', 'base01': '#4a4f5a'})

    class SolarizedDark(SolarizedDarkStyle):
        styles = make_style({**DARK_COLORS, 'base0': '#edeff3', 'base01': '#9ba2ae'})

    ui.add_css('.q-carousel__navigation-icon--active .q-icon {color:  #78909c !important; }')
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


def lesson(number: int, text: str) -> None:
    with nd.step():
        with ui.row(wrap=False, align_items='center') \
            .classes('absolute bottom-24 left-[50%] translate-x-[-50%] w-max text-lg p-4 gap-2 rounded '
                     f'border border-gray-500/20 bg-[#fff] dark:bg-black {TEXT_80} shadow-lg'):
            ui.markdown(f'**Takeaway #{number}:**')
            ui.markdown(text)


# --- 1. Title Slide ---
@nd.slide('''
    *(Wait for the audience to settle.)*
''')
def _():
    with nd.center_row():
        with ui.column().classes('absolute-center items-center text-center gap-4'):
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


# --- 2. The Question: JustPy vs NiceGUI ---
@nd.slide('''
    Let's start with some *code*.

    This is *JustPy* — a Python UI framework. It creates a card with a button and a label. When you click the button, the label text changes. *22 lines of code*.

    Five years ago, we were looking for a UI framework at *Zauberzeug* — that's the robotics company I work at, near Münster. We needed *dashboards* for our robots — motors, cameras, LEDs. And when we saw code like this, we thought: what if we build our own — one that's just... *nice*? What would that *look like*?

    ---

    *(step to NiceGUI code + result)*

    *This.* The same app. *8 lines*. And it *runs* — you can click the button right here.

    One reads like a *to-do list* — create this, configure that, add it here. The other reads like *the UI it describes*.

    The difference? It's about which *Python features* you choose to use. *"Readability counts."* *"Simple is better than complex."* *"Beautiful is better than ugly."* The *Zen of Python* — we just took it seriously.

    Now — this part was *obvious* from day one. Lean into Python's features and the API almost designs itself. The *hard part* was everything else. How do you handle *events*? *State*? *Styling*? How do you make *100 elements discoverable*? How do you let people *escape* your abstractions?

    Keeping it simple across 5 years and thousands of users — *that's* what this talk is about.
''')
def _():
    with slide_layout('What Makes an API Feel Pythonic?'):
        with ui.grid(columns='auto auto').classes('gap-x-8 gap-y-4 w-[95%]'):
            code_window(SNIPPETS / 'intro_justpy.py')

            with nd.step():
                @demo(mode='rows')
                def _():
                    with ui.card():
                        with ui.row():
                            ui.button('Click me', on_click=lambda: label.set_text('Hello PyCon! ❤️'))
                            label = ui.label('Hello Darmstadt!')


# --- 3. Who Am I ---
@nd.slide('''
    I'm *Falko Schindler*, lead developer of NiceGUI.

    I work at *Zauberzeug* — German for "magic tools" — a robotics company near Münster. We build *agricultural robots* like our Feldfreund here, and all the software to control them.

    NiceGUI started because we needed *dashboards for real hardware* — motors, cameras, LEDs — and nothing we found felt right.
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


# --- 4. The Sweet Spot: Streamlit vs NiceGUI ---
@nd.slide('''
    So JustPy was the *low-level* end. But there's also the *other extreme*.

    This is *Streamlit*. For a quick hello world, *nothing beats it*. Four lines — a label, a button, it runs. *Beautiful simplicity*.

    But try the *same interaction* we just saw — a button that *persistently* changes a label.

    ---

    Suddenly you need `session_state` — just to remember *one text*. You need `st.rerun()` to *trigger the update*. And the button? It's an *`if` statement*. Control flow *is* the event handling.

    To be fair: Streamlit made this choice *deliberately*. For *data apps* where you want stateless dashboards, the rerun model makes sense. But for *interactive, stateful UIs* — the kind we need for controlling robots — the framework deciding when your code runs? That's *too much magic*.

    We wanted the *sweet spot*: *high-level components*, *explicit state*, *real Python*. And this constraint — not too much magic, not too low-level — has guided every API decision since.
''')
def _():
    with slide_layout('The Sweet Spot'):
        with ui.grid(columns='1fr 1fr 1fr').classes('gap-4 w-[95%] items-start'):
            with ui.column().classes('gap-1'):
                ui.label('too low-level').classes(f'text-sm {TEXT_60}')
                code_window(SNIPPETS / 'intro_justpy.py')
            with nd.step(min=2), ui.column().classes('gap-1'):
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
                code_window(SNIPPETS / 'intro_streamlit.py')


# --- 5. Context Managers Are the Layout API ---
@nd.slide('''
    So let's talk about *specific lessons* we learned. The first one is probably the *biggest single insight* from 5 years of NiceGUI.

    UI has *hierarchy*. Cards contain rows. Rows contain labels. How do you *express* that in Python?

    On the left you see *HTML*. Tags nest inside tags. The indentation shows the structure. That's *actually good*.

    On the right — *NiceGUI*. Same structure. Same indentation. But instead of tags, we use Python's *`with` statement*.

    `with ui.card()` means: everything *within* this block is *inside* the card. The *shape of the code* mirrors the *shape of the UI*. And you can see it running right there.

    I like to say: the `with` statement is really a *"within"* statement.

    Now — this isn't just about UI. *Any domain that has hierarchy* can benefit from this. File systems, config trees, document structures — Python *already has the syntax* for nesting. You just have to *use it*.
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

        lesson(1, 'The with statement is a "within" statement — code shape mirrors UI shape.')


# --- 6. Method Chaining as Progressive Disclosure ---
@nd.slide('''
    Second lesson: *progressive disclosure* through method chaining.

    You start simple: `ui.button('Click')`. *Done*. One line, one button.

    But then you need *styling*. Then *behavior*. Then props for the underlying component library. Do you need a *completely different API* now?

    *No.* You just *chain*.

    Every method — `.classes()`, `.style()`, `.props()`, `.on()` — returns *self*. That's the *builder pattern* — each method returns the object itself, so you can keep chaining.

    *Beginners never see `.props()` until they need it.* And when they do need it, they don't have to *restructure* anything. They just add *one more dot* at the end.

    The lesson: *builder patterns* let users add complexity *without changing the structure* of their code. Beginners see *simplicity*, experts find *power* — without a *mode switch*.
''')
def _():
    with slide_layout('Method Chaining'):

        @demo
        def _():
            ui.button('Nice!', icon='face') \
                .props('outline') \
                .classes('m-auto') \
                .style('box-shadow: 0 0 1rem 0 rgba(0, 127, 255, 0.25)') \
                .on('mouseenter', lambda e: e.sender.classes('scale-125')) \
                .on('mouseleave', lambda e: e.sender.classes(remove='scale-125'))

        lesson(2, 'Builder patterns add complexity without changing code structure.')


# --- 7a. Lambdas & Callbacks ---
@nd.slide('''
    Third lesson: *event handling should be obvious*.

    Remember Streamlit's `if st.button(...)` pattern? Here's NiceGUI's answer:

    `on_click=lambda: ui.notify('Done.')` — *cause and effect in one line*.

    If your callback needs the *event object* — the value that changed, the element that was clicked — just add a *parameter*. NiceGUI looks at how many parameters your function takes and *passes what you need*.

    No special API. Just *Python lambdas*.
''')
def _():
    with slide_layout('Lambdas & Callbacks'):

        @demo
        def _():
            ui.number(value=41, on_change=lambda e: ui.notify(f'New value: {e.value}'))

            ui.button('Submit', on_click=lambda: ui.notify('Done.', type='positive'))


# --- 7b. Async / Await ---
@nd.slide('''
    And what if your handler needs to do something *slow*? An API call, an animation, a delay? Just make it *`async`*.

    `async def handle_click`. `await asyncio.sleep`. *No special framework API.* Your framework should accept whatever Python function you give it — sync *or* async.

    Let me click this button — "Wait for it..." — *(pause)* — "Click!"
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
    Now here's something more subtle: *auto-context*.

    I have two cards, each with a *plus button*. When I click the left button, a label appears — *in the left card*. When I click the right button — *in the right card*.

    I never told NiceGUI *where* to put those labels. It knows, because it tracks the *context* — which element, which slot, which *client*.

    That last one matters: NiceGUI is a *web framework*. Multiple users can visit the same app. Each user's events affect *only their own UI*.

    The lesson: callbacks should be as *lightweight* as the action they describe. If your event handling requires more *ceremony* than the event itself, *something is wrong*.
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

        lesson(3, 'Callbacks should be as lightweight as the action they describe.')


# --- 8. Decorators Make Patterns Declarative ---
@nd.slide('''
    So callbacks are lightweight. But what about *larger patterns* that repeat across your app?

    Fourth lesson: decorators make *patterns declarative*.

    A common pattern in UI development: you have a container, *state changes*, and you need to *clear it and rebuild* its contents. That's tedious. And *error-prone*.

    With `@ui.refreshable`, you just *describe* what the UI should look like. The decorator handles *clearing and rebuilding*.

    Here — I drag the slider. Below zero: *"Freezing"* in blue. Above zero: *"Cold"* in green. Above ten: *"Warm"* in orange.

    I didn't write any "clear container, then add label" logic. The `@ui.refreshable` decorator *does that for me*.

    The lesson: if you find yourself writing the *same scaffolding* around *different logic*, that's a *decorator waiting to happen*.
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

        lesson(4, 'Decorators like `@ui.refreshable` eliminate our users\' boilerplate.')


# --- 9. Design for the IDE ---
@nd.slide('''
    Fifth lesson, and this one is about something you *don't see* at runtime.

    Your API should be readable *before the user runs it*. In the *IDE*. In the *tooltip*. In the *auto-complete dropdown*.

    Look at this `Slider` class. Every parameter is *spelled out* — no `**kwargs`. The IDE can show you *exactly* what's available.

    Notice the *type hints* — `Handler`, `float | None` — that's what powers the whole IDE experience.

    And here's something I'm particularly proud of: *honest defaults*.

    Look at the `step` parameter: `DEFAULT_PROP | 1.0`. It tells you two things at once: this value *can be overridden globally*, and if it isn't, the fallback is *1.0*.

    How does that work? `DEFAULT_PROP` is a *sentinel* — a special placeholder object — with `__or__` overloaded, so the `| 1.0` *shows up in the signature*. The `@resolve_defaults` decorator resolves it at *call time*.

    A bit of *magic in the implementation* — but in service of a *crystal-clear API surface*.

    On the right you see what this looks like in practice — the IDE tooltip shows the *full story*.

    The lesson: every design choice should survive the *IDE test*. Your best documentation is the one the user *never has to open*.
''')
def _():
    with slide_layout('Design for the IDE'):
        with ui.grid(columns='1fr 1fr').classes('gap-x-8 gap-y-4 w-[95%] items-center'):
            code_window('''
                class Slider(ValueElement[float | None], DisableableElement):

                    @resolve_defaults
                    def __init__(
                        self,
                        *,
                        min: float,
                        max: float,
                        step: float = DEFAULT_PROP | 1.0,
                        value: float | None = DEFAULT_PROPS['model-value'] | None,
                        on_change: Handler[ValueChangeEventArguments[float | None]] | None = None,
                    ) -> None:
                        """Slider

                        This element is based on Quasar's `QSlider <https://quasar.dev/vue-components/slider>`_ component.

                        :param min: lower bound of the slider
                        :param max: upper bound of the slider
                        :param step: step size
                        :param value: initial value to set position of the slider
                        :param on_change: callback which is invoked when the user releases the slider
                        """
            ''')
            ui.interactive_image('assets/slider.png').classes('rounded shadow overflow-hidden')

        lesson(5, 'Your best documentation is the one users never have to open.')


# --- 10. Binding ---
@nd.slide('''
    Sixth lesson: work with Python's *object model*, don't fight it.

    UI shows data. Data changes. UI must *update*. The classic *two-way sync* nightmare.

    Some frameworks say: inherit from `Observable`. Use special `State` containers. *Wrap everything.*

    We tried cleverer approaches — *beautiful syntax*, but they broke. *Too fragile* for a mature library.

    So NiceGUI's approach is *explicit*. You pass the *object* and the *attribute name as a string*.

    Yes, passing strings means you lose some *refactoring safety*. We accept that trade-off — because it lets you bind to *any Python object* without requiring a special base class.

    Here — a number input, a label, and a slider. *All bound together.* Drag the slider, and *everything updates*.

    Here I'm binding UI elements to each other, but this works the same with a `@dataclass` — a `Temperature` class with a `value` field, say. Dataclasses, plain classes, other UI elements — *anything with attributes*. No registration. Just *Python objects*.

    The lesson: don't force users to *restructure their data model* for your framework. Work with what Python *already gives you*.
''')
def _():
    with slide_layout('Binding'):
        with ui.grid(columns='1fr 1fr').classes('gap-x-8 gap-y-4 w-[95%] items-start'):

            @demo(mode='rows')
            def _():
                number = ui.number(value=42)

                ui.label().bind_text_from(number, 'value', lambda v: f'T = {v:.0f}°C')

                ui.slider(min=0, max=100).bind_value(number)

            with nd.step():
                @demo(mode='rows')
                def _():
                    from dataclasses import dataclass

                    @dataclass
                    class Temperature:
                        value: float = 42

                    temp = Temperature()

                    ui.number().bind_value(temp, 'value')
                    ui.label().bind_text_from(temp, 'value', lambda v: f'T = {v:.0f}°C')
                    ui.slider(min=0, max=100).bind_value(temp, 'value')

        lesson(6, 'Work with Python\'s object model, don\'t fight it.')


# --- 11. Escape Hatches ---
@nd.slide('''
    Now let's zoom out from individual features and talk about *architecture*.

    NiceGUI sits on top of a *stack*.

    *(step through technologies one by one)*

    HTML. CSS. JavaScript. *Vue* — that's the JavaScript framework that powers our frontend. *Quasar* — a component library built on Vue. *Tailwind* — utility-first CSS. *FastAPI* — the Python web framework underneath. And at the bottom: *Python*.

    Every one of these layers is something you can *reach into directly*.

    `.classes('...')` gives you *Tailwind*. `.props('...')` gives you *Quasar*. `ui.html()` gives you *raw HTML*. `ui.run_javascript()` gives you *raw JavaScript* — need the browser's geolocation API? *One line*. And `app.routes` gives you the *full FastAPI*.

    We don't *hide* the web. We make it *optional*.

    And this is the key insight: users will *trust your abstractions* only if they know they can *bypass them*.

    The moment users feel *trapped* — the moment they hit a wall and there's no escape hatch — they *leave*.

    Always provide a *path to the layer below*.
''')
def _():
    with slide_layout('Escape Hatches'):
        def hatch(name: str, code: str) -> None:
            with nd.step():
                with ui.element().classes('row items-center text-xl'):
                    ui.label(name).classes('text-lg w-28')
                    ui.code(code, language='python').classes('text-sm').copy_button.delete()

        with ui.card():
            ui.label('NiceGUI').classes('text-2xl')
            ui.separator()
            hatch('HTML', "ui.html('<div>Raw HTML</div>')")
            hatch('CSS', "ui.element().classes('text-red')")
            hatch('JavaScript', "ui.run_javascript('alert(\"Hello\")')")
            hatch('Tailwind', "ui.label().classes('text-red')")
            hatch('Quasar', "ui.button().props('outline')")
            hatch('FastAPI', "app.get('/hello')")
            hatch('Python', 'class MyCustomElement(ui.element): ...')

        lesson(7, 'Always provide a path to the layer below.')


# --- 12. What Makes It "Nice" ---
@nd.slide('''
    We've been talking about *API design*. But niceness isn't just *technical*.

    The name — NiceGUI — is a *pun*. Nice GUI. Nice Guy. "A guy who tries to be *nice* to everyone and do things *right*."

    In our code review rules, *"prefer simple solutions"* is a *blocker*. Not a guideline. If a *simpler design* meets the requirements, the complex one is *rejected*. Full stop.

    We *dogfood relentlessly*. The entire nicegui.io website — documentation, live demos, interactive examples — is *built with NiceGUI*. We find our own bugs *before users do*.

    And when someone asks a question in our community, we reply with a *working code snippet*. Not just words. *Runnable code*. That's how we measure helpfulness.

    5 years. 15,000+ stars. About 120 UI elements. Frequent releases. A growing *ecosystem*.
''')
def _():
    with slide_layout('What Makes It "Nice"'):
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
@nd.slide('''
    So — what did we learn?

    *Python's language features are API design tools.* Context managers, decorators, lambdas, async, type hints, the object model — use them *deliberately*, not accidentally.

    *Find the sweet spot.* Not too much magic, not too low-level. The right abstraction lets your users think in *their domain*, not yours.

    And these lessons *aren't about UI*. CLI tools, ORMs, data pipelines, testing frameworks — *any Python API* benefits from the same thinking.

    *"Simple things should be simple. Complex things should be possible."* — Alan Kay.
''')
def _():
    with slide_layout('Takeaways'):
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
@nd.slide('''
    And to prove that point — here's *both* at the same time.

    *(gesture to the 3D point cloud)*

    A few lines of Python. An *animated 3D scene*. Simple things should be simple. Complex things should be *possible*.

    Thank you!

    You can find NiceGUI at *nicegui.io*, on *GitHub*, and on *Discord*. I'm happy to take *questions*.
''')
def _():
    with nd.center_row():

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


nd.run(
    setup=setup,
    classes='bg-[#fafbfc] dark:bg-[#0f1117]',
    props='control-color=blue-grey-2',
    time_limit=30 * 60,
    title='PyCon Germany 2026',
    uvicorn_reload_includes='*.py, *.css',
    dark=None,
)
