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


def setup():
    ui.add_css('.q-carousel__navigation-icon--active .q-icon {color:  # 78909c !important; }')
    ui.add_css(f'''
        {HtmlFormatter(nobackground=True, style=SolarizedLight).get_style_defs('div.codehilite')}
        {HtmlFormatter(nobackground=True, style=SolarizedDark).get_style_defs('.body--dark div.codehilite')}
    ''')


@contextmanager
def slide_layout(heading: str | None = None, *,
                 center_heading: str | None = None) -> Generator[None, None, None]:
    if heading:
        nd.heading(heading)
    if center_heading:
        nd.center_heading(center_heading)
    with nd.center_row():
        yield


# --- 1. Title Slide ---
@nd.slide()
def _():
    nd.note('''
        *(Wait for the audience to settle.)*
    ''')
    with nd.center_row():
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
@nd.slide()
def _():
    with slide_layout('What Makes an API Feel Pythonic?'):
        nd.note('''
            Let's start with *two pieces of code*.

            On the left, you see a Python UI framework called JustPy. It creates a card with a button and a label. When you click the button, the label text changes. *22 lines of code*.

            On the right — *the same app* in NiceGUI. *8 lines*. And it *runs* — you can click the button right here.

            Both do *exactly the same thing*. One reads like a *to-do list* — create this, configure that, add it here, add it there. The other reads like *the UI it describes*.

            So what's the *difference*? It's not about which framework is "better." It's about which *Python features* the designer chose to use.

            Look at the NiceGUI version. *"Readability counts"* — the code reads like the UI looks. *"Beautiful is better than ugly"* — the indentation *mirrors the hierarchy*. *"Simple is better than complex"* — 8 lines instead of 22. *"Flat is better than nested"* — no callback function just to set a text.

            These aren't my principles. They're from *the Zen of Python*. NiceGUI just takes them seriously.

            We've been building NiceGUI for *5 years* now. And this talk is about what we *learned* — about which Python language features make great APIs, and *why*.

            But first — I'm Falko Schindler, lead developer of NiceGUI. I work at *Zauberzeug*, a robotics company near Münster. We build agricultural robots, and NiceGUI started because we needed *dashboards for real hardware* — motors, cameras, LEDs.
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
@nd.slide()
def _():
    with slide_layout('The Sweet Spot'):
        nd.note('''
            That was the *low-level* end — JustPy. Now let me show you the *other extreme*.

            This is *Streamlit*. And honestly — for a quick hello world, *nothing beats it*. Four lines, and you have a label, a button, it runs. *Beautiful simplicity*.

            But now try the *same interaction* we just saw — a button that *persistently* changes a label.

            ---

            Suddenly you need `session_state` — just to remember *one text*. You need `st.rerun()` — to manually *trigger the update*. And the button itself? It's an *`if` statement*. Control flow *is* the event handling.

            Now — to be fair: Streamlit made this choice *deliberately*. For *data apps* where you want stateless dashboards, the rerun model makes sense. But for *interactive, stateful UIs* — the kind we need for controlling robots — the framework deciding when your code runs? That's *too much magic*.

            And JustPy was *too low-level*.

            We wanted the *sweet spot*: *high-level components*, *explicit state*, *real Python*.

            And this constraint — not too much magic, not too low-level — has guided *every API decision* we've made in the last 5 years.
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
@nd.slide()
def _():
    with slide_layout('Context Managers Are the Layout API'):
        nd.note('''
            So let's talk about *specific lessons* we learned. The first one is probably the *biggest single insight* from 5 years of NiceGUI.

            UI has *hierarchy*. Cards contain rows. Rows contain labels. How do you *express* that in Python?

            On the left you see *HTML*. Tags nest inside tags. The indentation shows the structure. That's *actually good*.

            On the right — *NiceGUI*. Same structure. Same indentation. But instead of tags, we use Python's *`with` statement*.

            `with ui.card()` means: everything *within* this block is *inside* the card. The *shape of the code* mirrors the *shape of the UI*. And you can see it running right there.

            I like to say: the `with` statement is really a *"within"* statement.

            Now — this isn't just about UI. *Any domain that has hierarchy* can benefit from this. File systems, config trees, document structures — Python *already has the syntax* for nesting. You just have to *use it*.
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
@nd.slide()
def _():
    with slide_layout('Method Chaining'):
        nd.note('''
            Second lesson: *progressive disclosure* through method chaining.

            You start simple: `ui.button('Click')`. *Done*. One line, one button.

            But then you need *styling*. Then *behavior*. Then props for the underlying component library. Do you need a *completely different API* now?

            *No.* You just *chain*.

            Every method — `.classes()`, `.style()`, `.props()`, `.on()` — returns *self*. That's the *builder pattern* — each method returns the object itself, so you can keep chaining.

            *Beginners never see `.props()` until they need it.* And when they do need it, they don't have to *restructure* anything. They just add *one more dot* at the end.

            The lesson: *builder patterns* let users add complexity *without changing the structure* of their code. Beginners see *simplicity*, experts find *power* — without a *mode switch*.
        ''')

        @demo
        def _():
            ui.button('Nice!', icon='face') \
                .props('outline') \
                .classes('m-auto') \
                .style('box-shadow: 0 0 1rem 0 rgba(0, 127, 255, 0.25)') \
                .on('mouseenter', lambda e: e.sender.classes('scale-125')) \
                .on('mouseleave', lambda e: e.sender.classes(remove='scale-125'))


# --- 6a. Lambdas & Callbacks ---
@nd.slide()
def _():
    with slide_layout('Lambdas & Callbacks'):
        nd.note('''
            Third lesson: *event handling should be obvious*.

            Remember Streamlit's `if st.button(...)` pattern? Here's NiceGUI's answer:

            `on_click=lambda: ui.notify('Done.')` — *cause and effect in one line*.

            If your callback needs the *event object* — the value that changed, the element that was clicked — just add a *parameter*. NiceGUI looks at how many parameters your function takes and *passes what you need*.

            No special API. Just *Python lambdas*.
        ''')

        @demo
        def _():
            ui.number(value=41, on_change=lambda e: ui.notify(f'New value: {e.value}'))

            ui.button('Submit', on_click=lambda: ui.notify('Done.', type='positive'))


# --- 6b. Async / Await ---
@nd.slide()
def _():
    with slide_layout('Async / Await'):
        nd.note('''
            And what if your handler needs to do something *slow*? An API call, an animation, a delay? Just make it *`async`*.

            `async def handle_click`. `await asyncio.sleep`. *No special framework API.* Your framework should accept whatever Python function you give it — sync *or* async.

            Let me click this button — "Wait for it..." — *(pause)* — "Click!"
        ''')

        @demo
        def _():
            import asyncio

            async def handle_click():
                ui.notify('Wait for it...')
                await asyncio.sleep(1)
                ui.notify('Click!')

            ui.button('Click me', on_click=handle_click)


# --- 6c. Auto-Context ---
@nd.slide()
def _():
    with slide_layout('Auto-Context'):
        nd.note('''
            Now here's something more subtle: *auto-context*.

            I have two cards, each with a *plus button*. When I click the left button, a label appears — *in the left card*. When I click the right button — *in the right card*.

            I never told NiceGUI *where* to put those labels. It knows, because it tracks the *context* — which element, which slot, which *client*.

            That last one matters: NiceGUI is a *web framework*. Multiple users can visit the same app. Each user's events affect *only their own UI*.

            The lesson: callbacks should be as *lightweight* as the action they describe. If your event handling requires more *ceremony* than the event itself, *something is wrong*.
        ''')

        @demo
        def _():
            with ui.row():
                with ui.card():
                    ui.button(icon='add', on_click=lambda: ui.label('Hello'))
                with ui.card():
                    ui.button(icon='add', on_click=lambda: ui.label('World'))


# --- 7. Decorators Make Patterns Declarative ---
@nd.slide()
def _():
    with slide_layout('Decorators'):
        nd.note('''
            So callbacks are lightweight. But what about *larger patterns* that repeat across your app?

            Fourth lesson: decorators make *patterns declarative*.

            A common pattern in UI development: you have a container, *state changes*, and you need to *clear it and rebuild* its contents. That's tedious. And *error-prone*.

            With `@ui.refreshable`, you just *describe* what the UI should look like. The decorator handles *clearing and rebuilding*.

            Here — I drag the slider. Below zero: *"Freezing"* in blue. Above zero: *"Cold"* in green. Above ten: *"Warm"* in orange.

            I didn't write any "clear container, then add label" logic. The `@ui.refreshable` decorator *does that for me*.

            The lesson: if you find yourself writing the *same scaffolding* around *different logic*, that's a *decorator waiting to happen*.
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


# --- 8. Design for the IDE ---
@nd.slide()
def _():
    with slide_layout('Design for the IDE'):
        nd.note('''
            Fifth lesson, and this one is about something you *don't see* at runtime.

            Your API should be readable *before the user runs it*. In the *IDE*. In the *tooltip*. In the *auto-complete dropdown*.

            First: a *flat namespace*. `ui.input` — not `ui.elements.input.TextInput`. Type `ui.` in your IDE and you can *browse everything*.

            Second: JustPy passes most things as `**kwargs`. The IDE *can't help you*. You're on your own with the docs. NiceGUI *spells out every parameter*. It's more code to *maintain*, but that's what shows up in the *tooltip*.

            ---

            Notice the *type hints* — `Handler`, `str | None` — that's what powers the whole IDE experience. And here's something I'm particularly proud of: *honest defaults*.

            Look at what your IDE shows you for the `color` parameter: `DEFAULT_PROP | 'primary'`.

            It tells you two things at once: this value *can be overridden globally*, and if it isn't, the fallback is *'primary'*.

            How does that work? `DEFAULT_PROP` is a *sentinel* — a special placeholder object — with `__or__` overloaded, so the `| 'primary'` *shows up in the signature*. The `@resolve_defaults` decorator resolves it at *call time*.

            A bit of *magic in the implementation* — but in service of a *crystal-clear API surface*.

            The lesson: every design choice should survive the *IDE test*. Your best documentation is the one the user *never has to open*.
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


# --- 9. Binding ---
@nd.slide()
def _():
    with slide_layout('Binding'):
        nd.note('''
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

        @demo
        def _():
            number = ui.number(value=42)

            ui.label().bind_text_from(number, 'value', lambda v: f'T = {v:.0f}°C')

            ui.slider(min=0, max=100).bind_value(number)


# --- 10. Escape Hatches ---
@nd.slide()
def _():
    with slide_layout('Escape Hatches'):
        nd.note('''
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


# --- 11. What Makes It "Nice" ---
@nd.slide()
def _():
    with slide_layout('What Makes It "Nice"'):
        nd.note('''
            We've been talking about *API design*. But niceness isn't just *technical*.

            The name — NiceGUI — is a *pun*. Nice GUI. Nice Guy. "A guy who tries to be *nice* to everyone and do things *right*."

            In our code review rules, *"prefer simple solutions"* is a *blocker*. Not a guideline. If a *simpler design* meets the requirements, the complex one is *rejected*. Full stop.

            We *dogfood relentlessly*. The entire nicegui.io website — documentation, live demos, interactive examples — is *built with NiceGUI*. We find our own bugs *before users do*.

            And when someone asks a question in our community, we reply with a *working code snippet*. Not just words. *Runnable code*. That's how we measure helpfulness.

            5 years. 15,000+ stars. About 120 UI elements. Frequent releases. A growing *ecosystem*.
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


# --- 12. Takeaways ---
@nd.slide()
def _():
    with slide_layout('Takeaways'):
        nd.note('''
            So — what did we learn?

            *Python's language features are API design tools.* Context managers, decorators, lambdas, async, type hints, the object model — use them *deliberately*, not accidentally.

            *Find the sweet spot.* Not too much magic, not too low-level. The right abstraction lets your users think in *their domain*, not yours.

            And these lessons *aren't about UI*. CLI tools, ORMs, data pipelines, testing frameworks — *any Python API* benefits from the same thinking.

            *"Simple things should be simple. Complex things should be possible."* — Alan Kay.
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


# --- 13. Thank You ---
@nd.slide()
def _():
    with nd.center_row():
        nd.note('''
            And to prove that point — here's *both* at the same time.

            *(gesture to the 3D point cloud)*

            A few lines of Python. An *animated 3D scene*. Simple things should be simple. Complex things should be *possible*.

            Thank you!

            You can find NiceGUI at *nicegui.io*, on *GitHub*, and on *Discord*. I'm happy to take *questions*.
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


nd.run(
    setup=setup,
    deck_classes='bg-[#fafbfc] dark:bg-[#0f1117]',
    deck_props='control-color=blue-grey-2',
    time_limit=30 * 60,
    title='PyCon Germany 2026',
    uvicorn_reload_includes='*.py, *.css',
)
