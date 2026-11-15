"""Web entry point for the original Project 3 stock visualizer."""
from datetime import date
from flask import Flask, render_template, request
from dotenv import load_dotenv
import api_client
import data_processor
from chart_generator import render_chart_svg
from stock_symbols import get_symbols

load_dotenv()
app = Flask(__name__)
SYMBOLS, SYMBOL_SOURCE = get_symbols()
FUNCTIONS = {
    "TIME_SERIES_INTRADAY": "Intraday (60-minute; may require premium access)",
    "TIME_SERIES_DAILY": "Daily",
    "TIME_SERIES_WEEKLY": "Weekly",
    "TIME_SERIES_MONTHLY": "Monthly",
}


@app.route("/", methods=["GET", "POST"])
def index():
    values = {"symbol": "AAPL", "chart_type": "Line", "function": "TIME_SERIES_DAILY",
              "start": "", "end": date.today().isoformat()}
    chart_svg = None
    error = None
    if request.method == "POST":
        values = {key: request.form.get(key, "").strip() for key in values}
        try:
            symbol = values["symbol"].upper()
            if symbol not in SYMBOLS:
                raise ValueError("Please select a stock from the dropdown.")
            values["symbol"] = symbol
            if values["chart_type"] not in ("Line", "Bar"):
                raise ValueError("Please select a valid chart type.")
            if values["function"] not in FUNCTIONS:
                raise ValueError("Please select a valid time series.")
            start = date.fromisoformat(values["start"])
            end = date.fromisoformat(values["end"])
            if start > end:
                raise ValueError("The start date must be on or before the end date.")
            if end > date.today():
                raise ValueError("The end date cannot be in the future.")
            data = api_client.fetch_stock_data(symbol, values["function"])
            series = data_processor.extract_series(data)
            filtered = data_processor.filter_by_date(series, start, end)
            if not filtered:
                raise ValueError("No stock data found for those dates. Try a more recent range or another time series.")
            dates, prices = data_processor.to_chart_data(filtered)
            chart_svg = render_chart_svg(symbol, values["chart_type"], dates, prices, start, end)
        except (ValueError, api_client.StockAPIError, KeyError, TypeError) as exc:
            error = str(exc)
        except Exception:
            app.logger.exception("Unexpected chart generation error")
            error = "An unexpected error occurred. Please try again."
    return render_template("index.html", symbols=SYMBOLS, source=SYMBOL_SOURCE,
                           functions=FUNCTIONS, values=values, chart_svg=chart_svg, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
