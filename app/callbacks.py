import os

# import pandas as pd
from dash.dependencies import Input, Output, State
from layouts import annotate_data_dir

from app import app
from scripts.annotator import get_data

# import sys
# from pathlib import Path


# SCRIPT_DIR = Path(__file__).resolve().parents[1]
# sys.path.append(str(SCRIPT_DIR))


@app.callback(Output("app-1-display-value", "children"), Input("app-1-dropdown", "value"))
def display_value(value):
    return 'You have selected "{}"'.format(value)


# @app.callback(Output("app-2-display-value", "children"), Input("app-2-dropdown", "value"))
# def display_value(value):
#    return 'You have selected "{}"'.format(value)


@app.callback(
    Output("selected-data-method", "children"),
    [
        Input("submit-val", "n_clicks"),
    ],
    [
        State("choose-data", "value"),
        State("choose-annotate-method", "value"),
        State("choose-sample-size", "value"),
    ],
)
def get_data_for_annotation(n_clicks, data, method, sample_size):
    if n_clicks == 0:
        return "No Data Selected"
    data_path = os.path.join(annotate_data_dir, data)
    df_annotate, df_annotated = get_data(data_path, method, sample_size)
    print(df_annotate.head())

    return f"Data is {data}, annotation method {method}"
