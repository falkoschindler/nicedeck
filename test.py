#!/usr/bin/env python3
from pathlib import Path

from nicegui import app, ui

import nicedeck as nd

PATH = Path(__file__).parent
ui.add_head_html(f'<style>{(PATH / "style.css").read_text()}</style>')
app.add_static_files('/fonts', PATH / 'fonts')


with nd.deck():
    with nd.slide():
        nd.heading('Event Handling: Async Lambdas')
        with nd.center_row():
            @nd.demo
            def demo():
                async def notify(value):
                    ui.notify(f'New value: {value}')

                ui.number(value=12, on_change=lambda e: ui.notify(f'New value: {e.value}'))

ui.run()
