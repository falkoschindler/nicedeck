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


def insight(text: str) -> None:
    with nd.step():
        with ui.row(wrap=False, align_items='center') \
            .classes('absolute bottom-24 left-[50%] translate-x-[-50%] w-max text-lg pl-0 pr-5 py-0 gap-4 rounded-xl '
                     f'border border-blue-500/20 bg-blue-50 dark:bg-blue-950 {TEXT_80} shadow-lg overflow-hidden'):
            ui.icon('lightbulb', size='sm').classes('bg-blue-500 text-white/90 size-12')
            ui.markdown(text)


# --- 1. Title Slide ---
@nd.slide('''
    (Wait for introduction by session chair.)
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
    Hello everyone,

    Let me ask you a question:

    - Which code would you prefer to review?
    - Which code would you prefer to maintain?
    - And what would Claude Code prefer?

    ---

    Both do the same:

    - Card, row, button, label
    - Click action

    Why does the right one feel nicer?

    - hierarchical code layout (todo list vs. UI structure)
    - method chaining
    - no page definition needed
    - lambda-friendly
    - 5 lines vs. 17

    This talk is about design decisions that make an API readable, Pythonic, and _nice_ to work with.

    And we look into several language feature you can use for your own projects.
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


# --- 3. Who Am I ---
@nd.slide('''
    Before we dive into the design insights, a quick introduction:

    I'm *Falko Schindler*, lead developer of NiceGUI, a web UI framework for Python.

    I work at a small robotics company near Münster called *Zauberzeug* — that's German for "magic tools".

    We build *agricultural robots* like our Feldfreund here, and all the software to control them.

    NiceGUI started because we needed *dashboards for real hardware* — motors, cameras, LEDs — and nothing we found felt right.

    Over the time of 5 years, we not only created one of the most popular Python UI frameworks,
    but continuously worked on refining its API to be more intuitive, more powerful, and more Pythonic.
    And that's what I want to share with you today.
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
    JustPy - the library on the left - was one candidate we looked into at the *low-level* end.

    ---

    On the other side: This is *Streamlit*.
    For a quick hello world, *nothing beats it*.
    A button, a label, it runs.

    Look how they use the *`if` statement* to handle a click.
    It works, but requires to *re-execute* the entire script on every interaction -
    which breaks *state management* and makes it really hard to build more complex UIs.

    ---

    Even our simple example becomes *unintuitive* when you want to

    - let the button update the label text and
    - put button and label in a row

    To be fair: Streamlit made this choice *deliberately*.
    For *data apps* where you want stateless dashboards, the rerun model makes sense.
    But for *interactive, stateful UIs* — the kind we need for controlling robots — it's *too much magic*.

    We wanted the *sweet spot*:
    *high-level components*, *explicit state*, *real Python*.
    And this constraint — *not too much magic, not too low-level* — has guided every API decision since.
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
    So let's talk about *7 specific insights* from those 5 years.

    The first one is probably the obvious and most powerful:
    UI has *hierarchy*.

    - Cards contain rows.
    - Rows contain labels.

    Left: *HTML*.
    Tags inside tags.
    Indentation shows structure.
    That's good!

    Right: *NiceGUI*.
    Same structure.
    Same indentation.

    But instead of tags, we use Python's *`with` statement*.
    `with ui.card()` means: everything *within* this block is *inside* the card.
    The *shape of the code* mirrors the *shape of the UI*.
    And you can see it running right there.

    ---

    So the `with` statement is really a *"within"* statement.

    Now — this isn't just about UI.
    *Any domain* that has hierarchy can benefit from this.

    - File systems,
    - config trees,
    - document structures

    Python *already has the syntax* for nesting. You just can *use it*.
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
    But context managers are just the *start*.
    When defining *UI* elements, you often have *many options* — styling, behavior, props for the underlying component library.
    This can end up in a *sea of parameters* — especially if you want to keep the simple use case simple.

    NiceGUI elements come with a handful of *parameters* and a *bunch of methods* for further configuration.
    These methods return *self*, so you can *chain* them...

    ---

    ...resulting in a *fluent API* that lets you create and configure a UI element in *one statement* without naming it.

    ---

    - Now the *two child elements* are clearly visible,
    - each line does *one thing* and one thing only, and
    - we *don't have to name* the button, and

    Moreover: By splitting the API this way, we achieve *progressive disclosure*:

    - Beginners see a *simple core* — just the parameters they need.
    - Experts can add props, styling, and detailed behavior.

    See the event handlers? They use *lambdas* — which leads us to the next insight...
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
    Code can get messy when you have to *name functions* for simple callbacks.

    On the left we see the the classic approach.

    - A label.
    - A number that shows a notification on change.
    - A button that updates a label on click.
    - Two separate named functions for the event handlers.

        It works, but there's a lot of *ceremony* for very little logic.

    ---

    On the right: the *same behavior*, but with lambdas.
    It defines *cause and effect in one line*.

    - Note this is only possible because NiceGUI offers methods like `set_text` that can be called within lambdas.
    - Furthermore, NiceGUI allows you to add or omit an event parameter.

        It inspects how many parameters your function takes and *passes what you need*.
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
    Similarly, NiceGUI automatically handles *synchronous and asynchronous* handlers.
    This can be an API call, an animation, a delay — *whatever* you need.
    For *robotic applications as well as web apps*, async support is crucial for keeping the UI *responsive*.
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
    Now here's something more subtle:

    We have two cards, each with a *plus button*.

    - When I click the left button, a label appears — *in the left card*.
    - When I click the right button — *in the right card*.

    I never told NiceGUI *where* to put those labels.
    It knows, because it tracks the *context* — which element, which slot, which *client*.

    That last one matters: NiceGUI is a *web framework*.
    Multiple users can visit the same app.
    Each user's events affect *only their own UI*.

    The insight from the last three slides:
    Callbacks should be as *lightweight* as the action they describe.
    If your event handling requires more *ceremony* than the event itself, *something is wrong*.
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
    So callbacks are lightweight.
    But what about *larger patterns* that repeat across your app?

    A common pattern we noticed in UI development:
    You have a container, *state changes*, and you need to *clear it and rebuild* its contents.
    That's tedious and *error-prone*.

    This is why we introduced the `@ui.refreshable` decorator.
    You just *describe* what the UI should look like.
    The decorator handles *clearing and rebuilding*.

    Here — I drag the slider.

    - Below zero: *"Freezing"* in blue.
    - Above zero: *"Cold"* in green.
    - Above ten: *"Warm"* in orange.

    I didn't write any "clear container, then add label" logic.
    The `@ui.refreshable` decorator *does that for me*.

    The insight:
    If you find yourself writing the *same scaffolding* around *different logic*,
    it might be a good candidate for a *decorator*.
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


# --- 9. Design for the IDE ---
@nd.slide('''
    For the next insight we're leaving the runtime and
    looking at something you *don't see* when you run the code — the *IDE experience*.

    Here's a simple button.

    - The default color is "primary" (your brand or signature color).
    - If I want a red button, I pass it explicitly. Easy.
    - But NiceGUI also supports *default props* — a way to change defaults *globally*.

        So the button has "primary" color again, without passing it.

    - But what if I *also* pass "red" color explicitly?

        What wins — the global default or the explicit argument? It's... *unclear*.
        And how can NiceGUI notice that the user passed "primary" explicitly?

    ---

    So how do you design an API that clearly distinguishes default values, global overrides, and explicit arguments?

    - A naive approach `None` as "use default value".

        But this signature doesn't communicate the default value.

        And sometimes `None` is a valid value — what if `None` is the default?

    - Better: introduce a special `DEFAULT` sentinel object.

        This avoids conflicts with `None`, but still doesn't communicate the actual default value.

    - After a few other attempts, this is what we came up with.

        This tells you *two things at once*: the value *can be overridden globally*,
        and if it isn't, the fallback is *"primary*.

    How?

    - `DEFAULT_PROP` is a *sentinel* with `__or__` allowing to put the default into *the signature*.

        A bit of *magic in the implementation* — but in service of a *more informative API surface*.
        And here's what that looks like in the IDE.

    - The *`@resolve_defaults`* decorator resolves it at *call time*.

    The insight:
    Your best documentation is the one the user *never has to open*.
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


# --- 10. Binding ---
@nd.slide('''
    UI shows data. Data changes. UI must *update*. The classic *two-way sync* nightmare.

    Some frameworks say: inherit from `Observable`. Use special `State` containers. *Wrap everything.*

    We tried cleverer approaches — *beautiful syntax*, but they broke. *Too fragile* for a mature library.

    So NiceGUI's approach is *explicit*. You pass the *object* and the *attribute name as a string*.

    Yes, passing strings means you lose some *refactoring safety*. We accept that trade-off — because it lets you bind to *any Python object* without requiring a special base class.

    Here — a number input, a label, and a slider. *All bound together.* Drag the slider, and *everything updates*.
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


# --- 10b. Binding to Any Object ---
@nd.slide('''
    Here I'm binding UI elements to each other, but this works the same with a `@dataclass` — a `Temperature` class with a `value` field, say. Dataclasses, plain classes, other UI elements — *anything with attributes*. No registration. Just *Python objects*.

    The insight: don't force users to *restructure their data model* for your framework. Work with what Python *already gives you*.
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
    So — let's step back.

    We've seen *seven insights*. But look at them again — stripped of all the NiceGUI specifics.

    Code shape should mirror *domain shape*. That's context managers.

    *Fluent APIs* let you configure an object in one statement. That's the builder pattern.

    Callbacks should be *lightweight*. That's lambdas and async.

    Turn repeated scaffolding into *decorators*.

    Design for the *IDE*, not just runtime.

    Work with the language's *object model*.

    Always provide *escape hatches* to the layer below.

    This isn't just about UI. It's about *Python API design*. Whether you're building a CLI, an ORM, a data pipeline — the same thinking applies.
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
                'Turn repeated scaffolding into decorators',
            ]),
            ('Discoverability', [
                'Design for the IDE, not just runtime',
                'Work with the language\'s object model',
            ]),
            ('Trust', [
                'Always provide escape hatches',
            ]),
        ]
        with ui.column():
            with ui.grid(columns='auto 1fr').classes('gap-x-8 gap-y-2 text-xl items-baseline'):
                for group, insights in groups:
                    ui.label(group).classes(f'font-bold {TEXT_60}').style(f'grid-row: span {len(insights)}')
                    for insight in insights:
                        ui.label(insight)
            with nd.step():
                ui.markdown("_This isn't just about UI — it's about **Python API design**._") \
                    .classes(f'{TEXT_80} mt-8 text-xl')


# --- 13. Beyond Code ---
@nd.slide('''
    But good *design principles* only survive if your *culture* enforces them.

    The name — NiceGUI — is a *pun*. Nice GUI. Nice Guy. "A guy who tries to be *nice* to everyone and do things *right*."

    In our code review rules, *"prefer simple solutions"* is a *blocker*. Not a guideline. If a *simpler design* meets the requirements, the complex one is *rejected*. Full stop.

    We *dogfood relentlessly*. The entire nicegui.io website — documentation, live demos, interactive examples — is *built with NiceGUI*. We find our own bugs *before users do*.

    And when someone asks a question in our community, we reply with a *working code snippet*. Not just words. *Runnable code*. That's how we measure helpfulness.

    Every PR, every issue reply — that's where design principles are *sustained or lost*.
''')
def _():
    with slide_layout('Beyond Code'):
        with ui.column().classes('items-center gap-8'):
            ui.label('NiceGUI = Nice Guy').classes('text-3xl')
            with nd.step(), ui.column().classes('items-center gap-4 text-xl'):
                ui.label('Always strive for simple solutions — for users and developers alike')
                ui.label('Build the NiceGUI website with NiceGUI')
                ui.label('Foster a welcoming open-source culture on GitHub and beyond')


# --- 14. Thank You ---
@nd.slide('''
    And to close — let me *show* you what I mean.

    *(gesture to the 3D point cloud)*

    A few lines of Python. An *animated 3D scene*. Context managers, lambdas, timers — everything we talked about.

    *"Simple things should be simple. Complex things should be possible."* — Alan Kay.

    Thank you! You can find NiceGUI at *nicegui.io*, on *GitHub*, and on *Discord*. I'm happy to take *questions*.
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
