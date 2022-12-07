import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

from components import *

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Visualization of Beijing Housing Data"


#########################
# CALLBACKS FOR PLOTS
#########################


@app.callback(Output("scatter-plot", "figure"), Input("range-slider", "value"))
def update_bar_chart(slider_range):
    low, high = slider_range
    mask = (df["totalPrice"] > low) & (df["totalPrice"] < high)
    fig = px.scatter(
        df[mask],
        y="tradeTime",
        x="totalPrice",
        color="totalPrice",
        size="totalPrice",
    )
    fig.update_layout(plot_bgcolor=BG_COLOR, height=SUBPLOT_HEIGHT)
    return fig


@app.callback(
    Output("pie", "figure"),
    Input("names", "value"),
)
def generate_chart(names):
    fig = px.pie(df, names=names, hole=0.3)
    return fig


#########################
# APP LAYOUT
#########################

app.layout = dbc.Container(
    style={"padding": "50px", "max-width": "100vw"},
    id="dashboard",
    fluid=True,
    children=[
        html.Div(
            html.H1("Beijing Housing Data Visualization"),
            style={
                "text-align": "center",
            },
        ),
        # ROW 1
        dbc.Row(
            [
                dbc.Col(
                    [
                        h2_title("Time vs Total Price: Scatter"),
                        time_price_scatter,
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        h2_title("Total Price: Scatter Map"),
                        dcc.Graph(figure=beijing_scatter_mapbox),
                    ],
                    width=6,
                ),
            ]
        ),
        # ROW 2
        dbc.Row(
            [
                dbc.Col(
                    [
                        h2_title("Average Prices over Time"),
                        dcc.Graph(figure=time_series_avg_price),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        h2_title("Housing Features: Donut Chart"),
                        pie_chart,
                    ],
                    width=6,
                ),
            ]
        ),
        # ROW 3
        dbc.Row(
            [
                dbc.Col(
                    [
                        h2_title("Average Total Price by Districts"),
                        dcc.Graph(figure=avg_total_district_bar),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        h2_title("Average Total Price by Building Structure"),
                        dcc.Graph(figure=building_str_price_bar_graph),
                    ],
                    width=6,
                ),
            ]
        ),
        # ROW 4
        dbc.Row(
            [
                h2_title("Area (m²) of Housing: Histogram"),
                dcc.Graph(figure=square_histogram),
            ]
        ),
    ],
)


#########################
# SERVER
#########################
if __name__ == "__main__":
    app.run_server(debug=True)
