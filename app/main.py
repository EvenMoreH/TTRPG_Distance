from fasthtml.common import * # type: ignore
from fasthtml.common import (
    Div, A, Input, Html, Head, Body, Title, Script, Link, Meta, H1, H3, serve,
)
import re

# for docker
app, rt = fast_app(static_path="static") # type: ignore

# for local
# app, rt = fast_app(static_path="app/static") # type: ignore


class Global_clean_string:
    """
    A utility class to clean strings globally.
    Used to remove white spaces and handle conversion of ',' to '.' for float.
    """
    clean_string: str

def string_cleaner(input_string: str):
    """
    Function that removes white spaces and handles conversion of ',' to '.' for float.
    """
    characters_to_remove = " "
    replace_dictionary = {",":"."}

    Global_clean_string.clean_string = input_string.translate(str.maketrans('', '', characters_to_remove))
    for old_character, new_character in replace_dictionary.items():
        Global_clean_string.clean_string = Global_clean_string.clean_string.replace(old_character, new_character)
    return Global_clean_string.clean_string

distance_form = Div(
Div(
    H1(
        "TTRPG Distance",
    ),
    A("RESET", href="/"),
    cls="grid",
    style="margin-bottom: 1vw;"
),
Div(
    Div(
        H3("Feet"),
        Input(
            id="feet",
            name="feet",
            type="text",
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
        H3("Meters"),
        Input(
            id="meters",
            name="meters",
            type="text",
            hx_post="/convert-m",
            hx_trigger="input",
            hx_include="#meters",
            cls="input-field",
        ),
        Div(
            id="results-mtf",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="output",
        ),
        Div(
            id="results-mth",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="output",
        ),
        cls="column",
    ),
    Div(
        H3("Hex"),
        Input(
            id="hex",
            name="hex",
            type="text",
            hx_post="/convert-hex",
            hx_trigger="input",
            hx_include="#hex",
            cls="input-field",
        ),
        Div(
            id="results-htf",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="output",
        ),
        Div(
            id="results-htm",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="output",
        ),
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
    # using if statement with .strip to check if input string (before conversion) is empty, if so - return no values
    if feet.strip() == "":
        return (
            Div(
                "",
                id="results-ftm",
                hx_swap_oob="true",
                hx_swap="innerHTML",
                cls="output",
            ),
            Div(
                "",
                id="results-fth",
                hx_swap_oob="true",
                hx_swap="innerHTML",
                cls="output",
            )
        )
    try:
        string_cleaner(feet)
        feet = Global_clean_string.clean_string
        feet_value = float(feet)
        meters = feet_value * 0.300003  # rounded to better utilize round method below
        hexes = feet_value / 5          # 1 hex/sq = 1 inch which is 5 ft
        return Div(
            f"{meters:.1f} meters",
            id="results-ftm",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="output",
        ), Div(
            f"{hexes:.1f} hexes",
            id="results-fth",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="output",
        )
    except ValueError:
        return Div(
        "Enter a number.",
        id="results-ftm",
        hx_swap_oob="true",
        hx_swap="innerHTML",
        cls="error",
        ), Div(
            "Enter a number.",
            id="results-fth",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="error",
        )

@rt("/convert-m")
def convert_m(meters: str):
    # using if statement with .strip to check if input string (before conversion) is empty, if so - return no values
    if meters.strip() == "":
        return (
            Div(
                "",
                id="results-mtf",
                hx_swap_oob="true",
                hx_swap="innerHTML",
                cls="output",
            ),
            Div(
                "",
                id="results-mth",
                hx_swap_oob="true",
                hx_swap="innerHTML",
                cls="output",
            )
        )
    try:
        string_cleaner(meters)
        meters = Global_clean_string.clean_string
        meters_value = float(meters)
        feet = meters_value * 3.33333   # rounded to better utilize round method below
        hexes = meters_value / 1.5      # 1 hex/sq = 1 inch which is 5 ft
        return Div(
            f"{feet:.1f} feet",
            id="results-mtf",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="output",
        ), Div(
            f"{hexes:.1f} hexes",
            id="results-mth",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="output",
        )
    except ValueError:
        return Div(
        "Enter a number.",
        id="results-mtf",
        hx_swap_oob="true",
        hx_swap="innerHTML",
        cls="error",
        ), Div(
            "Enter a number.",
            id="results-mth",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="error",
        )

@rt("/convert-hex")
def convert_hex(hex: str):
    # using if statement with .strip to check if input string (before conversion) is empty, if so - return no values
    if hex.strip() == "":
        return (
            Div(
                "",
                id="results-htf",
                hx_swap_oob="true",
                hx_swap="innerHTML",
                cls="output",
            ),
            Div(
                "",
                id="results-htm",
                hx_swap_oob="true",
                hx_swap="innerHTML",
                cls="output",
            )
        )
    try:
        string_cleaner(hex)
        hex = Global_clean_string.clean_string
        hex_value = float(hex)
        feet = hex_value * 5
        meters = hex_value * 1.5      # 1 hex/sq = 1 inch which is 5 ft
        return Div(
            f"{feet:.1f} feet",
            id="results-htf",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="output",
        ), Div(
            f"{meters:.1f} meters",
            id="results-htm",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="output",
        )
    except ValueError:
        return Div(
        "Enter a number.",
        id="results-htf",
        hx_swap_oob="true",
        hx_swap="innerHTML",
        cls="error",
        ), Div(
            "Enter a number.",
            id="results-htm",
            hx_swap_oob="true",
            hx_swap="innerHTML",
            cls="error",
        )

if __name__ == '__main__':
    # Important: Use host='0.0.0.0' to make the server accessible outside the container
    serve(host='0.0.0.0', port=5017)