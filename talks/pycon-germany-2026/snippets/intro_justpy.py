import justpy as jp


def hello_world():
    page = jp.QuasarPage()
    card = jp.QCard()
    row = jp.Div(classes='flex gap-4')

    def handle_click(sender, msg):
        label.text = 'Hello PyCon! ❤️'
    button = jp.QButton(text='Click me')
    button.on('click', handle_click)
    row.add(button)

    label = jp.Div(text='Hello Darmstadt!')
    row.add(label)

    card.add(row)
    page.add(card)
    return page


jp.justpy(hello_world)
