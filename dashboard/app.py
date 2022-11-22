import pandas as pd
import plotly.express as px
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

app = Dash(__name__)

#########################
# CALLBACKS FOR PLOTS
#########################


@app.callback(Output("scatter-plot", "figure"), Input("range-slider", "value"))
def update_bar_chart(slider_range):
    low, high = slider_range
    mask = (df["totalPrice"] > low) & (df["totalPrice"] < high)
    fig = px.scatter(
        df[mask],
        x="tradeTime",
        y="totalPrice",
        color="totalPrice",
        title="Trade Time vs Total Price(in 10k) Scatter Plot",
    )
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

app.layout = html.Div(
    children=[
        html.Div(
            html.H1("Beijing Housing Data Visualization"),
        ),
        data_summary,
        time_price_scatter,
        dcc.Graph(figure=time_series_avg_price),
        pie_chart,
        dcc.Graph(figure=avg_total_district_bar),
        dcc.Graph(figure=beijing_scatter_mapbox),
        dcc.Graph(figure=square_histogram),
        dcc.Graph(figure=building_str_price_bar_graph),
    ]
)


#########################
# SERVER
#########################
if __name__ == "__main__":
    app.run_server(debug=True)
