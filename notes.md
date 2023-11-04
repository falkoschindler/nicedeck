# Resources

- https://www.youtube.com/watch?v=0It8phQ1gkQ Streamlit PyData LA 2019

# Outline

## Background

- Who am I, what is Zauberzeug?
  [HQ picture]
  [robots]
- Core problem at Zauberzeug: Developing and controlling robots locally and remotely

## A new UI framework

- ODrive GUI
  https://discourse.odriverobotics.com/uploads/default/original/2X/6/6eb090388d280ab70d14bc507b08dbe186ac7a90.png
- Streamlit?

  ```py
  import streamlit as st

  st.write('Hello world!')
  ```

  ```py
  import streamlit as st

  if st.button('Say hello'):
      st.write('Hi!')
  ```

  But: constant reload, hard to manage state, hard to create something like timers

- Idea:

  - new UI toolbox based on a Flask/FastAPI app serving an Angular frontend?
  - more Pythonic than Streamlit
  - proof of concept after a few hours

- JustPy:

  - Name? Just Python --> "JustPy"?
  - https://justpy.io/
  - (almost) exactly what we were looking for
    (but with Vue instead of Angular (why not) and based on Quasar and Tailwind)
  - used as a basis for version 0.x
  - removed in 1.0
    (code base in poor condition, deprecated Vue and Quasar versions, too much overhead)

- The name "NiceGUI":
  - Our framework should be "nice" to use.
  - Nice guy:
    "a man who puts the needs of others before his own, avoids confrontations, does favors, provides emotional support, tries to stay out of trouble, and generally acts nicely towards others"
    https://en.wikipedia.org/wiki/Nice_guy
  - Pronounce as "nice guy"

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
