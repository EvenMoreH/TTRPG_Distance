import os
from fasthtml.common import (
    Body,
    Button,
    Div,
    H1,
    H3,
    Head,
    Html,
    Input,
    Link,
    Meta,
    P,
    Script,
    Title,
    fast_app,
    serve,
)
from dataclasses import dataclass

app, rt = fast_app(static_path="app/static")


@dataclass(frozen=True)
class ConversionRow:
    """Represents one rendered conversion result row."""

    label: str
    value: str


def clean_input_string(input_string: str) -> str:
    """Remove spaces and normalize commas for numeric parsing."""

    return input_string.replace(" ", "").replace(",", ".")


def parse_distance_value(raw_value: str) -> int:
    """Parse an integer-only distance input from the user."""

    cleaned_value = clean_input_string(raw_value)
    if cleaned_value == "":
        raise ValueError("Missing value")

    parsed_value = float(cleaned_value)
    if not parsed_value.is_integer():
        raise ValueError("Integer required")

    return int(parsed_value)


def format_decimal(value: float) -> str:
    """Format conversion values with one decimal place."""

    return f"{value:.1f}"


def get_server_port(default_port: int = 5017) -> int:
    """Read and validate the port from PORT environment variable."""

    raw_port = os.getenv("PORT", str(default_port))
    try:
        parsed_port = int(raw_port)
    except ValueError:
        return default_port

    if 1 <= parsed_port <= 65535:
        return parsed_port

    return default_port


def build_conversion_rows(value: int) -> list[ConversionRow]:
    """Create the six conversion results from one shared input value."""

    return [
        ConversionRow("Feet to meters", f"{value} feet = {format_decimal(value * 0.300003)} meters"),
        ConversionRow("Feet to hexes", f"{value} feet = {format_decimal(value / 5)} hexes"),
        ConversionRow("Meters to feet", f"{value} meters = {format_decimal(value * 3.33333)} feet"),
        ConversionRow("Meters to hexes", f"{value} meters = {format_decimal(value / 1.5)} hexes"),
        ConversionRow("Hexes to feet", f"{value} hexes = {format_decimal(value * 5)} feet"),
        ConversionRow("Hexes to meters", f"{value} hexes = {format_decimal(value * 1.5)} meters"),
    ]


def render_results(rows: list[ConversionRow]) -> Div:
    """Render the conversion rows in a compact stacked layout."""

    return Div(
        *[
            Div(
                P(row.label, cls="result-label"),
                P(row.value, cls="result-value"),
                cls="result-row",
            )
            for row in rows
        ],
        cls="results-list",
    )


distance_form = Div(
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
    Div(
        Input(
            id="distance-value",
            name="distance_value",
            type="number",
            step="1",
            inputmode="numeric",
            placeholder="Enter distance",
            hx_post="/convert",
            hx_trigger="input changed delay:150ms",
            hx_include="#distance-value",
            hx_target="#results-panel",
            hx_swap="innerHTML",
            cls="input-field input-main",
        ),
        Div("", id="results-panel", cls="results-panel"),
        cls="stack-layout"
    ),
    cls="container"
)

@rt("/")
def homepage():
    return Html(
        Head(
            Title("TTRPG Distance"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Link(rel="stylesheet", href="css/style.css"),
            Script(src="https://unpkg.com/htmx.org"),
            Link(rel="icon", href="images/favicon.ico", type="image/x-icon"),
            Link(rel="icon", href="images/favicon.png", type="image/png")
        ),
        Body(
            distance_form,
            Script(
                "document.getElementById('reset-btn').addEventListener('click', () => {"
                " const input = document.getElementById('distance-value');"
                " const results = document.getElementById('results-panel');"
                " if (input) input.value = '';"
                " if (results) results.innerHTML = '';"
                " });"
            )
        )
    )

@rt("/convert")
def convert(distance_value: str) -> Div:
    if distance_value.strip() == "":
        return Div("", cls="results-list")

    try:
        parsed_value = parse_distance_value(distance_value)
    except ValueError:
        return Div(
            "Enter a whole number.",
            cls="error",
        )

    return render_results(build_conversion_rows(parsed_value))


if __name__ == '__main__':
    serve(host='0.0.0.0', port=get_server_port())
