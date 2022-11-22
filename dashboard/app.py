# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

from components import data_summary

app = Dash(__name__)


app.layout = html.Div(
    children=[
        html.Div(
            html.H1("Beijing Housing Data Visualization"),
        ),
        data_summary,
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
