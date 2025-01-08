from fasthtml.common import * # type: ignore
from fasthtml.common import (
    Div, Form, Input, Button, Html, Head, Body, Title, Script, Link, Meta, H1, serve,
)
import re

# for docker
# app, rt = fast_app(static_path="static") # type: ignore

# for local
app, rt = fast_app(static_path="app/static") # type: ignore

class Global_clean_string:
    clean_string: str

def string_cleaner(temperature: str):
    characters_to_remove = " "
    replace_dictionary = {",":"."}

    Global_clean_string.clean_string = temperature.translate(str.maketrans('', '', characters_to_remove))
    for old_character, new_character in replace_dictionary.items():
        Global_clean_string.clean_string = Global_clean_string.clean_string.replace(old_character, new_character)
    return Global_clean_string.clean_string

distance_form = Div(
Div(
    H1("TTRPG Distance"),
    Button("Reset"),
    cls="row",
),
Div(
    Div(
        Input(name="placeholder - feet"),
        Div("conversion placeholder"),
        Div("conversion placeholder"),
        cls="column",
    ),
    Div(
        Input(name="placeholder - meters"),
        Div("conversion placeholder"),
        Div("conversion placeholder"),
        cls="column",
),
    Div(
        Input(name="placeholder - sq/hex"),
        Div("conversion placeholder"),
        Div("conversion placeholder"),
        cls="column",
    ),
    cls="row",
),
    cls="column",
)

@rt("/")
def homepage():
    return Html(
        Head(
            Title("TTRPG Distance"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Script(src="https://unpkg.com/htmx.org"),
            Link(rel="stylesheet", href="styles.css"),
            Link(rel="icon", href="images/favicon.ico", type="image/x-icon"),
            Link(rel="icon", href="images/favicon.png", type="image/png"),
        ),
        Body(distance_form)
    )


if __name__ == '__main__':
    # Important: Use host='0.0.0.0' to make the server accessible outside the container
    serve(host='0.0.0.0', port=5017) # type: ignore