"""Populate S&P 500 symbols from a CSV or public maintained CSV feed."""
import csv
import io
from pathlib import Path
import requests

CSV_URL = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
CSV_PATH = Path(__file__).with_name("stocks.csv")
# Only used if the CSV cannot be retrieved. The complete list is fetched or read from CSV.
FALLBACK = "AAPL ABBV ABT ADBE AMD AMGN AMZN AVGO BAC BRK.B CAT COST CRM CSCO CVX DIS GE GOOGL GOOG HD IBM INTC JNJ JPM KO LLY MA META MRK MSFT NFLX NVDA ORCL PEP PFE PG QCOM RTX SBUX T TGT TSLA UNH V VZ WMT XOM".split()


def parse_symbols(text):
    reader = csv.DictReader(io.StringIO(text.lstrip("\ufeff")))
    if not reader.fieldnames:
        return []
    column = next((name for name in reader.fieldnames if name.strip().lower() in ("symbol", "ticker", "ticker symbol")), None)
    if not column:
        return []
    return sorted({row[column].strip().upper() for row in reader if row.get(column) and row[column].strip()})


def get_symbols():
    if CSV_PATH.exists():
        try:
            symbols = parse_symbols(CSV_PATH.read_text(encoding="utf-8-sig"))
            if symbols:
                return symbols, "local CSV"
        except (OSError, UnicodeError, csv.Error):
            pass
    try:
        response = requests.get(CSV_URL, timeout=7)
        response.raise_for_status()
        symbols = parse_symbols(response.text)
        if symbols:
            try:
                CSV_PATH.write_text(response.text, encoding="utf-8")
            except OSError:
                pass
            return symbols, "online S&P 500 CSV"
    except requests.RequestException:
        pass
    return FALLBACK, "limited offline fallback (add stocks.csv for full list)"
