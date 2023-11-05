# Resources

- https://www.youtube.com/watch?v=0It8phQ1gkQ Streamlit PyData LA 2019

# Outline

## NiceGUI

- three-line hello world:

  ```py
  from nicegui import ui

  ui.label('Hello world!')

  ui.run()
  ```

  No command line tool to run,
  no build step,
  browser opens automatically.

  Easy for sharing code examples for documentation and Q&A.

- How to build hierarchies? `with` contexts vs. `add()` methods
  (HTML, NiceGUI, JustPy example)
- How to react on user input?
  lambda-friendly event registration:

  ```py
  ui.button('Click me', on_click=lambda: ui.notify('Hey!'))
  ```

  with/without args

  ```py
  ui.number(value=41, on_change=lambda e: ui.notify(f'new value: {e.value}'))
  ```

  with context

  ```py
  with ui.card():
    ui.button('Spawn', on_click=lambda: ui.label("I'm here!"))
  ```

  sync or async

  async lambdas

- builder pattern: `.style`, `.classes`, `.props`
- access to underlying frameworks:
  - Quasar props
  - other Quasar elements
  - Tailwind classes
  - CSS style
  - HTML elements
- Tailwind API
- binding
- `ui.refreshable`, `ui.state`
- `ui.markdown` with indented multiline string
