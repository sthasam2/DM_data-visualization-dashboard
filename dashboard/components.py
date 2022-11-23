import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dash_table, dcc, html


#########################
# DATA
#########################

# data frame

df = pd.read_csv("../assets/cleaned.csv")
df.drop(df[df["tradeYear"] < 2010].index, inplace=True)


df["district"] = df["district"].replace(
    {
        1: "Dongcheng",
        2: "Fengtai",
        3: "Tongzhou",
        4: "Daxing",
        5: "Fangshan",
        6: "Changping",
        7: "Chaoyang",
        8: "Haidian",
        9: "Shijingshan",
        10: "Xicheng",
        11: "Pinggu",
        12: "Mentougou",
        13: "Shunyi",
    }
)
df["buildingStructure"] = df["buildingStructure"].replace(
    {
        1: "unknown",
        2: "mixed",
        3: "brick and wood",
        4: "brick and concrete",
        5: "steel",
        6: "steel-concrete composite",
    }
)
df["buildingType"] = df["buildingType"].replace(
    {
        1: "tower",
        2: "bungalow",
        3: "combination of plate and tower",
        4: "plate",
    }
)
df["renovationCondition"] = df["renovationCondition"].replace(
    {
        1: "other",
        2: "rough",
        3: "Simplicity",
        4: "hardcover",
    }
)

# Scaling

df["totalPrice"] = df["totalPrice"].apply(lambda x: x * 10000)

# Average price every year and month

average_price_df = (
    df.groupby(["tradeYear", "tradeMonth"])["totalPrice"].mean().reset_index()
)
average_price_df["tradeTime"] = [
    f"{x}-{y}" for x, y in zip(average_price_df.tradeYear, average_price_df.tradeMonth)
]

avg_district = df.groupby(["district"])["totalPrice"].mean()
building_str = df.groupby(["buildingStructure"])["totalPrice"].mean()


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
        html.P("Filter by total price"),
        dcc.RangeSlider(
            id="range-slider",
            min=1000000,
            max=250000000,
            value=[1000000, 20000000],
        ),
    ]
)


time_series_avg_price = px.line(
    average_price_df,
    x="tradeTime",
    y="totalPrice",
    title="Average Annual Price",
    height=800,
)
time_series_avg_price.update_layout(
    plot_bgcolor="rgb(45, 45, 45)",
)
time_series_avg_price.update_xaxes(
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
        dcc.Graph(id="pie"),
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
    plot_bgcolor="rgb(45, 45, 45)",
    title_text="Average Total Price by Districts",
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
    width=1200,
    height=900,
    title="Scatter Map of the houses by price",
)

beijing_scatter_mapbox.update_layout(mapbox_style="open-street-map")
beijing_scatter_mapbox.update_layout(margin={"r": 50, "t": 50, "l": 100, "b": 10})


# Histogram of square feet of housing

square_histogram = px.histogram(df, x="square", range_x=[0, 300])
square_histogram.update_layout(
    plot_bgcolor="rgb(45, 45, 45)",
    title_text="Histogram of square feet of housing",
    title_x=0.5,
).update_yaxes(showgrid=False)


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
    plot_bgcolor="rgb(45, 45, 45)",
    title_text="Building structure vs price bar graph",
    title_x=0.5,
)
