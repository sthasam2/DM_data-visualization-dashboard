from dash import dash_table, Dash, html
import pandas as pd

# import dash_design_kit as ddk

df = pd.read_csv("../assets/cleaned.csv")


# Data table
data_summary = html.Div(
    children=[
        html.H2("Data table summary"),
        dash_table.DataTable(
            id="table",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.head().to_dict("records"),
            editable=True,
        ),
    ]
)

# Bar chart of data


#
