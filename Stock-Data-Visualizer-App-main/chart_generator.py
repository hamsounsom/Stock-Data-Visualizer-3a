"""Builds the pygal chart and opens it in the default browser."""
import os
import webbrowser
import pygal


def generate_chart(symbol, chart_type, dates, series, start, end):
    chart_class = pygal.Bar if chart_type == "Bar" else pygal.Line
    chart = chart_class(
        x_label_rotation=45,
        show_minor_x_labels=False,
        x_labels_major_count=min(len(dates), 15),
        width=1200,
        height=600,
    )
    chart.title = f"Stock Data for {symbol}: {start} to {end}"
    chart.x_labels = dates
    for name, values in series.items():
        chart.add(name, values)

    path = os.path.abspath(f"{symbol}_chart.svg")
    chart.render_to_file(path)
    webbrowser.open(f"file://{path}")
    return path


def render_chart_svg(symbol, chart_type, dates, series, start, end):
    """Render an SVG for embedding below the Flask form without opening a browser."""
    chart_class = pygal.Bar if chart_type == "Bar" else pygal.Line
    chart = chart_class(
        x_label_rotation=45,
        show_minor_x_labels=False,
        x_labels_major_count=min(len(dates), 15),
        width=1200,
        height=600,
        js=[],  # Self-contained SVG, no external script dependency.
    )
    chart.title = f"Stock Data for {symbol}: {start} to {end}"
    chart.x_labels = dates
    for name, values in series.items():
        chart.add(name, values)
    return chart.render(is_unicode=True)
