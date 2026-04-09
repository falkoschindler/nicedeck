# 5 Years of NiceGUI: What We Learned About Designing Pythonic UIs

**PyCon DE & PyData 2026** — April 16, 10:15 — Titanium Room

---

## Narrative Arc

**Thesis:** Python's language features aren't just convenient syntax — they're API
design primitives. If you lean into them, your API practically designs itself. If you
fight them, you get something that feels foreign.

**Structure:** Not a feature tour. Each section poses a design problem, shows how
Python's own features solve it, and extracts a transferable lesson. NiceGUI is the
case study, not the product pitch.

**Opening hook:** Start with the question, not the company. "What makes an API feel
Pythonic?" Show two snippets that do the same thing — one awkward, one obvious.
The difference is which Python features the designer chose to use.

**Closing punch:** The lessons apply far beyond UI frameworks. Anyone designing a
Python API — CLI tools, ORMs, data pipelines — can use these same primitives.

---

## 1. Title Slide

- "5 Years of NiceGUI: What We Learned About Designing Pythonic UIs"
- Falko Schindler — Zauberzeug
- nicegui.io / github.com/zauberzeug/nicegui

## 2. The Question (2 min)

Open cold — no introduction, no "hi my name is." Start with code.

**Show side by side:** JustPy code (left) vs NiceGUI code + live result (right).
See `snippets/intro_justpy.py` and the `@demo` in main.py.

- Show the running result below the NiceGUI code — the visual hierarchy (card > row > button + label)
  matches the code's indentation. That's the point.
- "Both do the same thing. One reads like a to-do list. The other reads like the UI it describes."
- "What's the difference? It's which Python features the designer chose to use."
- Some observations — the Zen of Python in action:
  - "Readability counts" — the code reads like the UI looks
  - "Beautiful is better than ugly" — indentation mirrors hierarchy
  - "Simple is better than complex" — 8 lines vs 22
- "We've been building NiceGUI for 5 years. Here's what we learned about letting Python do the design work."
- Now briefly: I'm Falko, Zauberzeug (robotics company near Münster), lead developer of NiceGUI.

## 3. The Sweet Spot (2 min)

Frame as a design constraint, not a history lesson.

- "That was the low-level end. Now the other extreme."

- **Streamlit** at its best — nothing beats this for a quick hello world:

  ```python
  import streamlit as st

  st.write('Hello Darmstadt!')

  if st.button('Click me'):
      st.write('Hello PyCon! ❤️')
  ```

- But try the same button interaction we just saw:

  ```python
  import streamlit as st

  if "label_text" not in st.session_state:
      st.session_state.label_text = "Hello Darmstadt!"

  with st.container(border=True):
      col1, col2 = st.columns(2)
      with col1:
          if st.button("Click me"):
              st.session_state.label_text = "Hello PyCon! ❤️"
              st.rerun()
      with col2:
          st.write(st.session_state.label_text)
  ```

- Step: show the full Streamlit version (from `snippets/intro_streamlit.py`) next to the simple one.

- `session_state` for a single text change, `st.rerun()` to update it,
  `if st.button(...)` — control flow as event handling.
  The framework decides when your code runs. That's the magic we wanted to avoid.

- "We wanted the sweet spot: high-level components, explicit state, real Python."

- Brief Zauberzeug context: we build robots — hardware, motors, cameras.
  We needed dashboards that work, not a thesis project on web frameworks.

- This constraint — not too much magic, not too low-level — guided every API decision since.

## 4. Lesson: Context Managers Are the Layout API (3 min)

The deeper insight behind what the audience just saw.

- You already saw this — Python's indentation _is_ the hierarchy:

  ```python
  with ui.card():
      with ui.row():
          ui.label('Hello')
          ui.label('world!')
  ```

- "The `with` statement is really a 'within' statement."

- Show side-by-side: HTML vs NiceGUI — same nesting, different syntax.
  HTML has it too — hierarchy _should_ be visible in code. JustPy lost it, NiceGUI got it back.

- Live demo: build a nested layout, audience sees the code shape matches the screen.

- **Lesson:** if your domain has hierarchy, Python already has the syntax for it.
  File systems, config trees, document structures — `with` blocks work everywhere.

## 5. Lesson: Method Chaining as Progressive Disclosure (3 min)

How to handle complexity without forcing it upfront.

- **Problem:** a `ui.button('Click')` is nice and simple. But then you need styling.
  Then behavior. Do you need a completely different API now?

- No. You chain:

  ```python
  ui.button('Nice!', icon='face') \
      .props('outline') \
      .classes('m-auto') \
      .style('box-shadow: 0 0 1rem 0 rgba(0, 127, 255, 0.25)') \
      .on('mouseenter', lambda e: e.sender.classes('scale-125'))
  ```

- Each method returns `self` — nothing new, it's the builder pattern.
  But it means beginners never see `.props()` until they need it.

- Four layers of depth: Pure Python → Tailwind/UnoCSS → Quasar props → raw HTML/JS.
  You go deeper only when you choose to.

- Live demo: start with a plain button, chain styling and events onto it.

- **Lesson:** builder patterns let users add complexity without restructuring code.
  Beginners see simplicity, experts find power — without a mode switch.

## 6. Lesson: Lambdas Make Events Obvious (3 min)

The most Pythonic thing about NiceGUI.

- **Problem:** user clicks a button — what happens?

- Remember the `if st.button(...)` pattern? NiceGUI's answer: cause and effect in one line.

  ```python
  ui.button('Submit', on_click=lambda: ui.notify('Done.', type='positive'))
  ui.number(value=41, on_change=lambda e: ui.notify(f'New value: {e.value}'))
  ```

- With or without event argument — NiceGUI inspects the signature and does the right thing.

- **Auto-context:** when you create UI in a handler, it appears in the right place.

  ```python
  with ui.row():
      with ui.card():
          ui.button(icon='add', on_click=lambda: ui.label('Hello'))
      with ui.card():
          ui.button(icon='add', on_click=lambda: ui.label('World'))
  ```

- Click the left button → label appears in the left card. No explicit parent tracking.

- Context means more than just the container — it also tracks the _client_.
  Multiple users visit the same app → each user's events affect only their own UI.
  NiceGUI is a web framework after all.

- Live demo: both examples.

- **Lesson:** callbacks should be as lightweight as the action they describe.
  If your event handling requires more ceremony than the event itself, something is wrong.

## 7. Lesson: Async/Await Just Works (2 min)

Short and sweet — this one sells itself.

- **Problem:** handler needs to do something slow — API call, animation, delay.

- Just make it `async`:

  ```python
  async def handle_click():
      ui.notify('Wait for it...')
      await asyncio.sleep(1)
      ui.notify('Click!')

  ui.button('Click me', on_click=handle_click)
  ```

- No special framework API. No `run_in_executor`. No callback pyramids.
  If Python's `async/await` works, your framework should accept it.

- Live demo.

- **Lesson:** don't invent concurrency models when Python already has one.

## 8. Lesson: Decorators Make Patterns Declarative (3 min)

Where NiceGUI borrows from FastAPI — and where it goes further.

- **Problem 1:** routing — how do you map URLs to pages?

  - `@ui.page('/settings')` — if you know FastAPI, you already know this.
  - Familiar patterns reduce learning curves.

- **Problem 2:** reactivity — UI that updates when state changes.

  - Common pattern: clear a container, rebuild its contents. Tedious and error-prone.

  - `@ui.refreshable` makes it declarative:

    ```python
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
    ```

- The decorator handles clearing and rebuilding. You just describe what the UI should look like.

- Live demo: drag the slider, watch the label change color.

- **Lesson:** decorators turn recurring patterns into declarations.
  If you find yourself writing the same scaffolding around different logic, that's a decorator waiting to happen.

## 9. Lesson: Design for the IDE (2 min)

No live demo, but show IDE screenshots — auto-complete dropdown, tooltip for `ui.button()`.

The unifying principle: your API should be readable _before_ the user runs it —
in the IDE, in the tooltip, in the auto-complete dropdown.

- **Flat namespace:** `ui.input`, not `ui.elements.input.TextInput`. Type `ui.` and browse everything.

- **Type hints for chaining:** `ui.button().classes()` returns `Button`, not `Element`.
  So you stay in the right type context throughout the chain.

- **Explicit signatures over `**kwargs`:** JustPy passes everything as `\*\*kwargs` —
  the IDE can't help you, you're on your own with the docs.
  NiceGUI spells out every parameter. More code to maintain, but that's what shows up in the tooltip.

- **Honest defaults:**

  ```python
  class Button(...):
      @resolve_defaults
      def __init__(self,
                  text: str = '', *,
                  on_click: Handler[ClickEventArguments] | None = None,
                  color: str | None = DEFAULT_PROP | 'primary',
                  icon: str | None = DEFAULT_PROP | None,
                  ) -> None:
  ```

  Behind the curtain, `DEFAULT_PROP` is a sentinel with `__or__` overloaded so the `| 'primary'`
  shows up in the signature. `@resolve_defaults` does the actual resolution at call time.
  The IDE tooltip tells the full story: "default prop, or if not overridden globally, 'primary'."
  A bit of magic in the implementation — but in service of a crystal-clear API surface.

- "Your best documentation is the one the user never has to open."

- **Lesson:** every design choice should survive the IDE test —
  does auto-complete, the tooltip, the signature tell the user what they need?

## 10. Lesson: Binding Leverages Python's Object Model (3 min)

The "it just works with your existing code" moment.

- **Problem:** UI shows data. Data changes. UI must update. Classic two-way sync nightmare.

- Some frameworks: inherit from `Observable`, use special `State` containers, wrap everything.
  (Looking at you, Reflex.)

- We actually tried the magical version first: `car.driver.bind(person.name)` —
  using monkey-patching and caller introspection to figure out what you meant.
  (See github.com/zauberzeug/binding.) Beautiful syntax, but too fragile for a mature library.

- NiceGUI's approach is explicit: pass the object and attribute name as strings.

  ```python
  number = ui.number(value=42)
  ui.label().bind_text_from(number, 'value', lambda v: f'T = {v:.0f}°C')
  ui.slider(min=0, max=100).bind_value(number)
  ```

- Works with any object that has attributes — dataclasses, plain classes, other UI elements.
  No base class required. No registration. Just Python objects.

- The `lambda v: ...` transform is optional — for formatting, unit conversion, etc.

- Live demo: drag the slider, watch the label and number input update.

- **Lesson:** don't force users to restructure their data model for your framework.
  Work with what Python already gives you.

## 11. Escape Hatches: Trust Through Transparency (2 min)

The architectural philosophy behind all the layers.

- Show the stack visually (stepped reveal):
  NiceGUI → HTML, CSS, JavaScript, Vue, Quasar, Tailwind/UnoCSS, FastAPI, Python
- "Every layer here is something you can reach into directly."
- `.classes('...')` → Tailwind. `.props('...')` → Quasar. `ui.html()` → raw HTML.
  `ui.run_javascript()` → raw JS. `app.routes` → full FastAPI.
- "We don't hide the web. We make it optional."
- "Users trust your abstractions only if they know they can bypass them."
- **Lesson:** always provide a path to the layer below.
  The moment users feel trapped, they leave.

## 12. Beyond API: What Makes It "Nice" (2 min)

The human side — culture and discipline.

- The name: NiceGUI = Nice Guy — "a guy who tries to be nice to everyone and do things right."
- "Prefer simple solutions" — this is in our code review rules as a **blocker**.
  Not a guideline. If a simpler design meets the requirements, the complex one is rejected.
- Dogfooding: nicegui.io — the entire website, docs, live demos — is built with NiceGUI.
  We find our own bugs before users do.
- Community: when someone asks a question, we reply with a working code snippet.
  Helpfulness is measured in runnable examples.
- Numbers: 5 years, 15k+ stars, ~120 UI elements, frequent releases, growing ecosystem.

## 13. Takeaways (1 min)

No new information — just crystallize.

- **Python's language features are API design tools.** Context managers, decorators, lambdas,
  async, type hints, the object model — use them deliberately, not accidentally.
- **Find the sweet spot.** Not too much magic, not too low-level.
  The right abstraction is the one that lets your users think in their domain, not yours.
- **These lessons aren't about UI.** CLI tools, ORMs, data pipelines, testing frameworks —
  any Python API benefits from the same thinking.
- Closing quote: "Simple things should be simple, complex things should be possible." — Alan Kay

## 14. Thank You / Q&A

- Surprise ending: a 3D scene. The audience has seen flat UI for 30 minutes — then this:

  ```python
  from time import time
  import numpy as np
  from nicegui import ui

  def generate_data():
      u, v = np.meshgrid(np.linspace(0, 1), np.linspace(0, 1))
      w = np.sin(5 * u + time()) * np.cos(5 * v + time())
      rgb = np.dstack([u, v, w / 2 + 0.5]).reshape(-1, 3)
      return rgb * [6, 6, 2] - [3.5, 2, 0], rgb

  with ui.scene(grid=False, background_color='white'):
      wave = ui.scene.point_cloud([], point_size=0.1)

  ui.timer(0.05, lambda: wave.set_points(*generate_data()))

  ui.run()
  ```

- "Simple things should be simple. Complex things should be possible."
  This is both — a 3D scene in a few lines of Python.

- Links: nicegui.io, GitHub, Discord
