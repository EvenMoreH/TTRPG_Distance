# TTRPG Distance

TTRPG Distance is a lightweight web app for converting tabletop movement values
between feet, meters, and hexes in real time.

The interface is intentionally minimal: enter a whole number and the app
immediately displays six conversion results.

## Features

- Fast, live conversion using HTMX input events
- Conversion pairs for feet, meters, and hexes
- Whole-number input validation with clear error feedback
- Responsive single-page UI suitable for desktop and mobile
- Reset button to clear input and results quickly

## Tech Stack

- Python 3.12+
- python-fasthtml
- fastlite
- uvicorn
- HTMX

## Project Structure

```text
.
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── app/
	├── main.py
	└── static/
		├── css/
		│   └── style.css
		└── images/
```

## How It Works

The app serves a single page at `/` with one numeric input.

As the user types:

1. HTMX sends the input value to `POST /convert`
2. The backend validates that the value is a whole number
3. The server returns rendered HTML rows with conversion results
4. The results panel updates without a full page reload

The server binds to `0.0.0.0` and reads the port from the `PORT`
environment variable. If `PORT` is missing or invalid, it falls back to `5017`.

## Conversion Rules

For an input value `n`:

- Feet to meters: `n * 0.300003`
- Feet to hexes: `n / 5`
- Meters to feet: `n * 3.33333`
- Meters to hexes: `n / 1.5`
- Hexes to feet: `n * 5`
- Hexes to meters: `n * 1.5`

Displayed values are formatted to one decimal place.

## Input Behavior

- Empty input clears results
- Decimal values are rejected
- Comma decimal separators are normalized before parsing
- Error message shown for invalid values: `Enter a whole number.`

## License

This project is licensed under the terms in [LICENSE](LICENSE).
