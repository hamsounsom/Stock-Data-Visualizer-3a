"""Module 13: Unit tests for Project 3 Stock Data Visualizer inputs.

Place this file beside input_handler.py and run:
    python -m unittest mod13_YOURPAWPRINT.py -v
"""

import unittest
from datetime import date
from unittest.mock import patch

from input_handler import (
    get_symbol,
    get_chart_type,
    get_time_series,
    _get_date,
    get_date_range,
)


class TestStockVisualizerInputs(unittest.TestCase):
    """Check the five user inputs required by Project 3."""

    # 1. Stock symbol: uppercase, 1 to 7 letters.
    def test_symbol_accepts_valid_letters(self):
        with patch("builtins.input", return_value="AAPL"):
            self.assertEqual(get_symbol(), "AAPL")

    def test_symbol_capitalizes_lowercase(self):
        with patch("builtins.input", return_value="msft"):
            self.assertEqual(get_symbol(), "MSFT")

    def test_symbol_rejects_invalid_characters_and_lengths(self):
        # Empty, digits, and 8-letter symbols are rejected before a valid one.
        with patch("builtins.input", side_effect=["", "AAPL1", "ABCDEFGH", "GOOGL"]) as mocked:
            self.assertEqual(get_symbol(), "GOOGL")
            self.assertEqual(mocked.call_count, 4)

    # 2. Chart type: one digit, either 1 or 2.
    def test_chart_type_accepts_both_choices(self):
        for choice, expected in (("1", "Bar"), ("2", "Line")):
            with self.subTest(choice=choice):
                with patch("builtins.input", return_value=choice):
                    self.assertEqual(get_chart_type(), expected)

    def test_chart_type_rejects_invalid_choices(self):
        with patch("builtins.input", side_effect=["0", "3", "12", "a", "1"]) as mocked:
            self.assertEqual(get_chart_type(), "Bar")
            self.assertEqual(mocked.call_count, 5)

    # 3. Time series: one digit, from 1 through 4.
    def test_time_series_accepts_all_four_choices(self):
        options = {
            "1": "TIME_SERIES_INTRADAY",
            "2": "TIME_SERIES_DAILY",
            "3": "TIME_SERIES_WEEKLY",
            "4": "TIME_SERIES_MONTHLY",
        }
        for choice, expected in options.items():
            with self.subTest(choice=choice):
                with patch("builtins.input", return_value=choice):
                    self.assertEqual(get_time_series(), expected)

    def test_time_series_rejects_invalid_choices(self):
        with patch("builtins.input", side_effect=["0", "5", "22", "x", "2"]) as mocked:
            self.assertEqual(get_time_series(), "TIME_SERIES_DAILY")
            self.assertEqual(mocked.call_count, 5)

    # 4. Start date: a real calendar date written as YYYY-MM-DD.
    def test_start_date_accepts_valid_date(self):
        with patch("builtins.input", return_value="2026-10-01"):
            self.assertEqual(_get_date("Start date: "), date(2026, 10, 1))

    def test_start_date_rejects_invalid_dates(self):
        with patch("builtins.input", side_effect=["2026/10/01", "2026-13-01", "2026-02-30", "2026-10-01"]) as mocked:
            self.assertEqual(_get_date("Start date: "), date(2026, 10, 1))
            self.assertEqual(mocked.call_count, 4)

    # 5. End date: valid date that cannot be before the start date.
    def test_end_date_accepts_valid_date_range(self):
        with patch("builtins.input", side_effect=["2026-10-01", "2026-10-28"]):
            self.assertEqual(get_date_range(), (date(2026, 10, 1), date(2026, 10, 28)))

    def test_end_date_rejects_date_before_start(self):
        with patch("builtins.input", side_effect=["2026-10-01", "2026-09-30", "2026-10-28"]) as mocked:
            self.assertEqual(get_date_range(), (date(2026, 10, 1), date(2026, 10, 28)))
            self.assertEqual(mocked.call_count, 3)

    def test_end_date_rejects_invalid_calendar_date(self):
        with patch("builtins.input", side_effect=["2026-10-01", "2026-02-30", "2026-10-28"]) as mocked:
            self.assertEqual(get_date_range(), (date(2026, 10, 1), date(2026, 10, 28)))
            self.assertEqual(mocked.call_count, 3)


if __name__ == "__main__":
    unittest.main()
