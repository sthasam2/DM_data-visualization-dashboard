import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dash_table, dcc, html

from components import (
    df,
    data_summary,
    time_price_scatter,
    time_series_avg_price,
    pie_chart,
    avg_total_district_bar,
    beijing_scatter_mapbox,
    square_histogram,
    building_str_price_bar_graph,
)

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
        title="Trade Time vs Total Price Scatter Plot",
        size="totalPrice",
    )
    fig.update_layout(plot_bgcolor="rgb(45, 45, 45)", height=800)
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
    id="dashboard",
    children=[
        html.Div(
            html.H1("Beijing Housing Data Visualization"),
            style={
                "text-align": "center",
            },
        ),
        html.Div(
            html.H2("Data Table Summary"),
            style={
                "text-align": "center",
                "padding": "100px 40px 0 40px",
            },
        ),
        data_summary,
        html.Div(
            html.H2("Time vs Total Price Scatter"),
            style={
                "text-align": "center",
                "padding": "100px 40px 0 40px",
            },
        ),
        time_price_scatter,
        html.Div(
            html.H2("Average Prices over Time"),
            style={
                "text-align": "center",
                "padding": "100px 40px 0 40px",
            },
        ),
        dcc.Graph(figure=time_series_avg_price),
        html.Div(
            html.H2("Total Price in Beijing Scatter"),
            style={
                "text-align": "center",
                "padding": "100px 40px 0 40px",
            },
        ),
        dcc.Graph(figure=beijing_scatter_mapbox),
        html.Div(
            html.H2("Different Housing Features Pie Chart"),
            style={
                "text-align": "center",
                "padding": "100px 40px 0 40px",
            },
        ),
        pie_chart,
        html.Div(
            html.H2("Average Total Price in Districts"),
            style={
                "text-align": "center",
                "padding": "100px 40px 0 40px",
            },
        ),
        dcc.Graph(figure=avg_total_district_bar),
        html.Div(
            html.H2("Average Total Price per Building Structure"),
            style={
                "text-align": "center",
                "padding": "100px 40px 0 40px",
            },
        ),
        dcc.Graph(figure=building_str_price_bar_graph),
        html.Div(
            html.H2("Square m of Housing Histogram"),
            style={
                "text-align": "center",
                "padding": "100px 40px 0 40px",
            },
        ),
        dcc.Graph(figure=square_histogram),
    ],
)


#########################
# SERVER
#########################
if __name__ == "__main__":
    app.run_server(debug=True)
