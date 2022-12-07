import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html

from data import *

SUBPLOT_HEIGHT = 700
BG_COLOR = "#d7e1ee"


#########################
# COMPONENTS
#########################

# Data table
data_summary = html.Div(
    children=[
        dbc.Table.from_dataframe(
            df.head(),
            id="table",
            responsive=True,
            size="md",
        ),
    ]
)

# scatter plot trade time vs price
time_price_scatter = html.Div(
    [
        dcc.Graph(id="scatter-plot"),
        dcc.RangeSlider(
            id="range-slider",
            min=500000,
            max=250000000,
            value=[500000, 20000000],
        ),
    ]
)


time_series_avg_price = px.line(
    average_price_df,
    x="tradeTime",
    y="totalPrice",
    height=SUBPLOT_HEIGHT,
)
time_series_avg_price.update_layout(plot_bgcolor=BG_COLOR,).update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list(
            [
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all"),
            ]
        )
    ),
)

# construction piechart

pie_chart = html.Div(
    [
        html.P("Category"),
        dcc.Dropdown(
            id="names",
            options=[
                "constructionTime",
                "livingRoom",
                "drawingRoom",
                "kitchen",
                "bathRoom",
                "buildingType",
                "renovationCondition",
                "buildingStructure",
                "elevator",
                "fiveYearsProperty",
            ],
            value="livingRoom",
            clearable=False,
        ),
        dcc.Graph(id="pie", style={"height": f"{SUBPLOT_HEIGHT}px"}),
    ]
)


# Bar graph of Average Total Price By Districts

avg_total_district_bar = (
    px.bar(
        avg_district,
        x=avg_district.index,
        y=avg_district,
        color="totalPrice",
        text_auto=True,
    )
    .update_xaxes(type="category", categoryorder="total descending", showgrid=False)
    .update_yaxes(showgrid=False)
)
avg_total_district_bar.update_layout(
    plot_bgcolor=BG_COLOR,
    title_x=0.5,
)


## Scatter map

beijing_scatter_mapbox = px.scatter_mapbox(
    df,
    lon="Lng",
    lat="Lat",
    zoom=10,
    color="price",
    size="totalPrice",
    color_continuous_scale=px.colors.cyclical.IceFire,
    # width=1200,
    height=SUBPLOT_HEIGHT,
)
beijing_scatter_mapbox.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 50, "t": 50, "l": 100, "b": 10},
)


# Histogram of square feet of housing

square_histogram = px.histogram(df, x="square", range_x=[0, 300])
square_histogram.update_layout(plot_bgcolor=BG_COLOR, title_x=0.5,).update_yaxes(
    showgrid=False
).update_traces(xbins=dict(size=5))


# Bar Graph showing building structure and the price

building_str_price_bar_graph = (
    px.bar(
        building_str,
        x=building_str.index,
        y=building_str,
        color="totalPrice",
        text_auto=True,
    )
    .update_xaxes(type="category", categoryorder="total descending", showgrid=False)
    .update_yaxes(showgrid=False)
)
building_str_price_bar_graph.update_layout(
    plot_bgcolor=BG_COLOR,
    title_x=0.5,
)


def h2_title(title: str):
    return html.Div(
        html.H2(title),
        style={
            "text-align": "center",
            "padding": "100px 40px 0 40px",
        },
    )
