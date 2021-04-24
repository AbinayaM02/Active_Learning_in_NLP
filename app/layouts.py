import os
from pathlib import Path

import dash_core_components as dcc
import dash_html_components as html

colors = {"background": "#000000", "text": "#7FDBFF"}
class_map = {1: "World News", 2: "Sports", 3: "Business", 4: "Sci/Tech", 0: "Not Sure"}
annotate_data_dir = Path(__file__).resolve().parents[1] / "annotate_data/20210421"

initial_layout = html.Div(
    # style={"backgroundColor": colors["background"]},
    children=[
        html.H1(
            children="annotate.it",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        html.Div(
            [
                html.Label(
                    [
                        "Choose Data to annotate",
                        dcc.Dropdown(
                            id="choose-data",
                            options=[
                                {"label": i, "value": i} for i in os.listdir(annotate_data_dir)
                            ],
                            style={"width": "50%"},
                        ),
                    ],
                    style={"width": "50%"},
                ),
                html.Label(
                    [
                        "Choose Method to Annotate",
                        dcc.Dropdown(
                            id="choose-annotate-method",
                            options=[
                                {"label": "Random Sampling", "value": "random"},
                                {
                                    "label": "Least Confidence Sampling",
                                    "value": "least",
                                },
                                {"label": "Margin Sampling", "value": "margin"},
                                {"label": "Entropy Base Sampling", "value": "entropy"},
                            ],
                            style={"width": "50%"},
                        ),
                    ],
                    style={"width": "50%"},
                ),
            ],
            style={"display": "flex", "columnCount": 2},
        ),
        html.Button(children="Submit", id="submit-val", n_clicks=0),
        html.H1(id="selected-data-method"),
    ]
)

layout1 = html.Div(
    [
        html.H3("App 1"),
        dcc.Dropdown(
            id="app-1-dropdown",
            options=[{"label": "App 1 - {}".format(i), "value": i} for i in ["NYC", "MTL", "LA"]],
        ),
        html.Div(id="app-1-display-value"),
        dcc.Link("Go to App 2", href="/apps/app2"),
    ]
)

layout2 = html.Div(
    [
        html.H3("App 2"),
        dcc.Dropdown(
            id="app-2-dropdown",
            options=[{"label": "App 2 - {}".format(i), "value": i} for i in ["NYC", "MTL", "LA"]],
        ),
        html.Div(id="app-2-display-value"),
        dcc.Link("Go to App 1", href="/apps/app1"),
    ]
)
