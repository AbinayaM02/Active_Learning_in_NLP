from dash.dependencies import Input, Output, State
import pandas as pd
import os
from layouts import annotate_data_dir
from app import app


@app.callback(
    Output("app-1-display-value", "children"), Input("app-1-dropdown", "value")
)
def display_value(value):
    return 'You have selected "{}"'.format(value)


@app.callback(
    Output("app-2-display-value", "children"), Input("app-2-dropdown", "value")
)
def display_value(value):
    return 'You have selected "{}"'.format(value)


@app.callback(
    Output("selected-data-method", "children"),
    [
        Input("submit-val", "n_clicks"),
    ],
    [
        State("choose-data", "value"),
        State("choose-annotate-method", "value"),
    ],
)
def get_data(n_clicks, data, method):
    df = pd.read_csv(os.path.join(annotate_data_dir, data))
    print(df.head())

    return f"Data is {data}, annotation method {method}"
