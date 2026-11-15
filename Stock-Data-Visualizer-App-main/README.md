# Stock Data Visualizer — Project 3a

This extends the team's Project 3 command-line Python app into a Flask website running in Docker. The original `main.py` CLI remains available.

## Run with Docker Desktop

1. Install and launch Docker Desktop.
2. Copy `.env.example` to `.env` in this folder.
3. Edit `.env` and replace `replace_with_your_key` with your own Alpha Vantage API key (do **not** commit `.env` to GitHub).
4. Open a terminal in this folder and run:

   ```bash
   docker compose up --build
   ```

5. Visit http://localhost:5000 in your browser.
6. Select a stock, chart type, time series, and dates. Click **Generate chart**. The chart appears under the form.
7. Stop the app with Ctrl+C, or `docker compose down` from another terminal.

## Run without Docker

```bash
python -m pip install -r requirements.txt
python app.py
```

You still need a `.env` file with your API key. Open http://localhost:5000.

## S&P stock symbols

At startup, `stock_symbols.py` reads `stocks.csv` if present. Otherwise it downloads a maintained S&P 500 constituents CSV and caches it locally. It supports a CSV column named `Symbol`, `Ticker`, or `Ticker Symbol`. If offline with no CSV, a **limited** fallback list is shown (not the full index). For fully offline grading, place the professor's `stocks.csv` from `stocks.csv.zip` next to `app.py` before building the image. This file was not included with the uploaded project.

## API notes

- API requests use the original `api_client.py` and processing uses the original `data_processor.py`.
- Alpha Vantage may restrict intraday or full-history data for free accounts. Errors appear on the page rather than crashing the app.
- A recent daily date range is recommended for a first test.
- The original CLI entry point `python main.py` still works.

## GitHub submission

Create your own GitHub repository, upload the source code, Docker files, HTML template, and README. Never upload `.env`. Verify the site runs locally and demonstrate a chart with your own API key.
