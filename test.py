#!/usr/bin/env python3
from pathlib import Path

from nicegui import app, ui

import nicedeck as nd

PATH = Path(__file__).parent
ui.add_head_html(f'<style>{(PATH / "style.css").read_text()}</style>')
app.add_static_files('/fonts', PATH / 'fonts')


with nd.deck():
    with nd.slide():
        ui.label('Slide 1')
        nd.note('This is note 1')
    with nd.slide():
        ui.label('Slide 2')
        nd.note('This is note 2')
    with nd.slide():
        ui.label('Slide 3')
        nd.note('This is note 3')


ui.run()
