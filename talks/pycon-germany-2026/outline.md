# 5 Years of NiceGUI: What We Learned About Designing Pythonic UIs

**PyCon DE & PyData 2026** — April 16, 10:15 — Titanium Room

## 1. Title Slide

- "5 Years of NiceGUI: What We Learned About Designing Pythonic UIs"
- Falko Schindler — Zauberzeug
- nicegui.io / github.com/zauberzeug/nicegui

## 2. The Origin Story (2 min)

- Zauberzeug: robotics company near Münster — "magic tools"
- The problem: needed UIs for motors, cameras, LEDs
- Streamlit: too much magic (implicit reruns, hidden state)
- JustPy: too low-level (raw HTML elements)
- The Goldilocks moment: what if we build something in the middle?

## 3. Three Lines to Delight (2 min)

- The minimal NiceGUI app: `from nicegui import ui` / `ui.label(...)` / `ui.run()`
- Auto-opens browser, hot-reload, live web UI — zero config
- Live demo: show it running
- Design principle: front-load delight, defer complexity

## 4. Python Feature: Context Managers for Composition (4 min)

- "The shape of the code mirrors the hierarchy of the DOM"
- `with ui.card():` / `with ui.row():` — indentation = nesting
- Compare: HTML nesting, JustPy's `add()` calls, NiceGUI's `with` blocks
- The `with` statement as a "within" statement
- Live demo: nested layout

## 5. Python Feature: Method Chaining / Builder Pattern (3 min)

- `.classes()` / `.style()` / `.props()` / `.on()` — fluent API
- Progressive complexity: pure Python → Tailwind → Quasar → raw HTML/JS
- No restructuring needed to add styling or behavior
- Live demo: building up a styled, interactive button step by step

## 6. Python Feature: Lambdas & Callbacks for Event Handling (3 min)

- `on_click=lambda: ...` — Pythonic, not framework-magic
- With/without event arguments
- Auto-context: UI created in handlers appears in the right place
- Contrast with Streamlit's rerun model
- Live demo: button clicks, input changes

## 7. Python Feature: Async/Await for Non-Blocking UIs (2 min)

- Sync and async handlers work seamlessly
- `async def handle_click()` with `await asyncio.sleep()`
- No special API — just Python's native async
- Live demo: async notification sequence

## 8. Python Feature: Decorators for Routing & Reactivity (3 min)

- `@ui.page('/')` — FastAPI-style routing, familiar to Python devs
- `@ui.refreshable` — declarative UI updates
- `ui.state()` — borrowed from React, feels Pythonic
- Live demo: refreshable counter or multi-page app

## 9. Python Feature: Type Hints for IDE Support (2 min)

- Flat `ui.*` namespace — type `ui.` and discover everything
- Type hints power auto-complete and inline docs
- Generic element types for proper chaining return types
- Design choice: IDE as the primary discovery mechanism

## 10. Python Feature: Dataclasses & Binding for State (3 min)

- `bind_value()` / `bind_text_from()` — connect UI to data models
- Works with any object that has attributes (dataclasses, plain classes)
- Two-way and one-way binding with transform functions
- Live demo: slider bound to label and number input

## 11. Python Feature: Sentinel Patterns for Discoverable APIs (2 min)

- Optional parameters that distinguish "not provided" from `None`
- Enables cleaner APIs: omit vs. explicitly set to None
- Small detail, big impact on usability

## 12. Escape Hatches: Trust Through Transparency (2 min)

- Layer 1: Pure Python (`ui.button()`, `ui.label()`)
- Layer 2: Tailwind CSS (`.classes('...')`, `.tailwind.*`)
- Layer 3: Quasar props (`.props('outlined dense')`)
- Layer 4: Raw HTML/JS/CSS (`ui.html()`, `ui.run_javascript()`, FastAPI routes)
- "Users trust your abstractions only if they can bypass them"
- Styling choice: Tailwind or UnoCSS — developer picks the engine
- Standing on the shoulders of giants: Vue, Quasar, Tailwind, FastAPI

## 13. Beyond API: What Makes It "Nice" (2 min)

- The pun: NiceGUI ↔ Nice Guy — "tries to be nice to everyone"
- "Prefer simple solutions" — not a README platitude, a code review blocker
- Dogfooding: nicegui.io is built with NiceGUI
- Community culture: respond with code, not just words
- Ecosystem integration: `ui.anywidget` bridges Jupyter widgets into NiceGUI
- 5 years, 15k+ stars, ~100 UI elements, weekly releases

## 14. Takeaways / Closing (1 min)

- Python's language features aren't just convenient — they're API design tools
- Context managers, decorators, lambdas, async, type hints — use them deliberately
- The Goldilocks principle: not too much magic, not too low-level
- "Developer experience is a consequence of caring about the same things your users care about"

## 15. Thank You / Q&A

- Live demo: `ui.label('Thank you.')` — because even slides are NiceGUI
- Links: nicegui.io, GitHub, Discord
