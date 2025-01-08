from fasthtml.common import * # type: ignore
from fasthtml.common import (
    Div, Form, Input, Button, Html, Head, Body, Title, Script, Link, Meta, H1, serve,
)
import re

# for docker
# app, rt = fast_app(static_path="static") # type: ignore

# for local
app, rt = fast_app(static_path="app/static") # type: ignore

# TODO:
#   1. Build remaining endpoints to convert:
#       A. meters to ft and hex
#       B. hexes to ft and meters
#   2. Fix styling and layout
#       A. .input-field needs to be added and configured within styles.css file
#   3. Ready for Docker

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
    H1(
        "TTRPG Distance",
        style="margin-bottom: 1vw;",
    ),
    Form(
            Button(
            "Reset",
            type="submit",
        ),
        action="/",
        method="get",
        style="max-height: 0px",
    ),
    cls="row",
),
Div(
    Div(
        Input(
            id="feet",
            name="feet",
            type="text",
            placeholder="Enter feet",
            hx_post="/convert-ft",
            hx_trigger="input",
            hx_include="#feet",
            cls="input-field",
        ),
        Div(
            id="results-ftm",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="output",
        ),
        Div(
            id="results-fth",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="output",
        ),
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

@rt("/convert-ft")
def convert_ft(feet: str):
    try:
        feet_value = float(feet)
        meters = feet_value * 0.3       # rounded to better utilize round method below
        meters = round(meters * 2) / 2  # result will always be either .0 or .5
        hexes = feet_value / 5          # 1 hex/sq = 1 inch which is 5 ft
        return Div(
            f"Meters: {meters:.1f}",
            id="results-ftm",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="output",
        ), Div(
            f"Hexes: {hexes:.1f}",
            id="results-fth",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="output",
        )
    except ValueError:
        return Div(
        "Invalid input. Please enter a numeric value.",
        id="results-ftm",
        hx_swap_oob="true",
        hx_swap="innerHTML",
        cls="output",
        ), Div(
            "Invalid input. Please enter a numeric value.",
            id="results-fth",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="output",
        )

if __name__ == '__main__':
    # Important: Use host='0.0.0.0' to make the server accessible outside the container
    serve(host='0.0.0.0', port=5017)