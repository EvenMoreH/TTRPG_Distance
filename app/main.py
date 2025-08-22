from fasthtml.common import * # type: ignore

# for docker
app, rt = fast_app(static_path="static") # type: ignore

# for local
# app, rt = fast_app(static_path="app/static") # type: ignore

class Global_clean_string:
    """A utility class to clean strings globally.
    Removes white spaces and converts commas to dots for float parsing.
    """
    clean_string: str

def string_cleaner(input_string: str):
    """Remove spaces and convert commas to dots for float conversion."""
    clean = input_string.replace(' ', '')
    clean = clean.replace(',', '.')
    Global_clean_string.clean_string = clean
    return clean


distance_form = Div(
    # form header
    Div(
        H1("TTRPG Distance", cls="title"),
        Button(
            "RESET",
            id="reset-btn",
            type="button",
            cls="btn"
        ),
        cls="header"
    ),
    # cards grid
    Div(
        Div(
            H3("Feet", cls="card-title"),
            Input(
                id="feet", name="feet", type="number",
                hx_post="/convert-ft", hx_trigger="input",
                hx_include="#feet", cls="input-field"
            ),
            Div("", id="results-ftm", hx_swap_oob="true", hx_swap="innerHTML", cls="output"),
            Div("", id="results-fth", hx_swap_oob="true", hx_swap="innerHTML", cls="output"),
            cls="card"
        ),
        Div(
            H3("Meters", cls="card-title"),
            Input(
                id="meters", name="meters", type="number",
                hx_post="/convert-m", hx_trigger="input",
                hx_include="#meters", cls="input-field"
            ),
            Div("", id="results-mtf", hx_swap_oob="true", hx_swap="innerHTML", cls="output"),
            Div("", id="results-mth", hx_swap_oob="true", hx_swap="innerHTML", cls="output"),
            cls="card"
        ),
        Div(
            H3("Hex", cls="card-title"),
            Input(
                id="hex", name="hex", type="number",
                hx_post="/convert-hex", hx_trigger="input",
                hx_include="#hex", cls="input-field"
            ),
            Div("", id="results-htf", hx_swap_oob="true", hx_swap="innerHTML", cls="output"),
            Div("", id="results-htm", hx_swap_oob="true", hx_swap="innerHTML", cls="output"),
            cls="card"
        ),
        cls="grid-layout"
    ),
    cls="container"
)

@rt("/")
def homepage():
    return Html(
        Head(
            Title("TTRPG Distance"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Link(rel="stylesheet", href="css/output.css"),
            Script(src="https://unpkg.com/htmx.org"),
            Link(rel="icon", href="images/favicon.ico", type="image/x-icon"),
            Link(rel="icon", href="images/favicon.png", type="image/png")
        ),
        Body(
            distance_form,
            # script to reset input fields on client using a bit of JS
            Script(
                "document.getElementById('reset-btn').addEventListener('click', () => {"
                " document.querySelectorAll('.input-field').forEach(i => i.value = '');"
                " document.querySelectorAll('.output').forEach(o => o.innerHTML = '');"
                " document.querySelectorAll('.error').forEach(e => { e.innerHTML = ''; e.classList.remove('error'); e.classList.add('output'); });"
                " });"
            )
        )
    )

@rt("/convert-ft")
def convert_ft(feet: str):
    if feet.strip() == "":
        return (
            Div("", id="results-ftm", hx_swap_oob="true", hx_swap="innerHTML", cls="output"),
            Div("", id="results-fth", hx_swap_oob="true", hx_swap="innerHTML", cls="output")
        )
    try:
        string_cleaner(feet)
        feet_value = float(Global_clean_string.clean_string)
        meters = feet_value * 0.300003
        hexes = feet_value / 5
        return (
            Div(f"{meters:.1f} meters", id="results-ftm", hx_swap_oob="true", hx_swap="innerHTML", cls="output"),
            Div(f"{hexes:.1f} hexes", id="results-fth", hx_swap_oob="true", hx_swap="innerHTML", cls="output")
        )
    except ValueError:
        err_ftm = Div("Enter a number.", id="results-ftm", hx_swap_oob="true", hx_swap="innerHTML", cls="error")
        err_fth = Div("", id="results-fth", hx_swap_oob="true", hx_swap="innerHTML", cls="error")
        return err_ftm, err_fth

@rt("/convert-m")
def convert_m(meters: str):
    if meters.strip() == "":
        return (
            Div("", id="results-mtf", hx_swap_oob="true", hx_swap="innerHTML", cls="output"),
            Div("", id="results-mth", hx_swap_oob="true", hx_swap="innerHTML", cls="output")
        )
    try:
        string_cleaner(meters)
        meters_value = float(Global_clean_string.clean_string)
        feet = meters_value * 3.33333
        hexes = meters_value / 1.5
        return (
            Div(f"{feet:.1f} feet", id="results-mtf", hx_swap_oob="true", hx_swap="innerHTML", cls="output"),
            Div(f"{hexes:.1f} hexes", id="results-mth", hx_swap_oob="true", hx_swap="innerHTML", cls="output")
        )
    except ValueError:
        err_mtf = Div("Enter a number.", id="results-mtf", hx_swap_oob="true", hx_swap="innerHTML", cls="error")
        err_mth = Div("", id="results-mth", hx_swap_oob="true", hx_swap="innerHTML", cls="error")
        return err_mtf, err_mth

@rt("/convert-hex")
def convert_hex(hex: str):
    if hex.strip() == "":
        return (
            Div("", id="results-htf", hx_swap_oob="true", hx_swap="innerHTML", cls="output"),
            Div("", id="results-htm", hx_swap_oob="true", hx_swap="innerHTML", cls="output")
        )
    try:
        string_cleaner(hex)
        hex_value = float(Global_clean_string.clean_string)
        feet = hex_value * 5
        meters = hex_value * 1.5
        return (
            Div(f"{feet:.1f} feet", id="results-htf", hx_swap_oob="true", hx_swap="innerHTML", cls="output"),
            Div(f"{meters:.1f} meters", id="results-htm", hx_swap_oob="true", hx_swap="innerHTML", cls="output")
        )
    except ValueError:
        err_htf = Div("Enter a number.", id="results-htf", hx_swap_oob="true", hx_swap="innerHTML", cls="error")
        err_htm = Div("", id="results-htm", hx_swap_oob="true", hx_swap="innerHTML", cls="error")
        return err_htf, err_htm


if __name__ == '__main__':
    serve(host='0.0.0.0', port=5017)
