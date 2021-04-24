import dash_core_components as dcc
import dash_html_components as html
import os
from pathlib import Path
from dash_html_components.Button import Button

from dash_html_components.Ol import Ol
from dash_html_components.P import P

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
                                {"label": i, "value": i}
                                for i in os.listdir(annotate_data_dir)
                            ],
                            style={"width": "33%"},
                        ),
                    ],
                    style={"width": "33%"},
                ),
                html.Label(
                    [
                        "Annotation Method",
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
                            style={"width": "33%"},
                        ),
                    ],
                    style={"width": "33%"},
                ),
                html.Label(
                    [
                        "Sample Size",
                        dcc.Input(id="choose-sample-size", value=100, type="number"),
                    ],
                    style={"width": "33%"},
                ),
            ],
            style={"display": "flex", "columnCount": 3},
        ),
        dcc.Link(
            html.Button(children="Submit", id="submit-val", n_clicks=0),
            href="/instruction",
        ),
        html.H1(id="selected-data-method"),
    ]
)

instruction_layout = html.Div(
    [
        html.H1(
            "Annotation Instruction",
            style={
                "color": "blue",
            },
        ),
        html.H2("""In this exercise we will be labeling news into one of the below 4 category. 
                In case, news is ambigous, please choose option `Not Sure`"""),
        # html.P(),
        html.Ol([html.Li("World News")]),
        dcc.Link(
            html.Button(children="Next", id="annotate-val", n_clicks=0),
            href="/annotate",
        ),
    ]
)

annotation_layout = html.Div(
    [
        html.H2("Title:"),
        html.H2(id="title", ),
        html.P("IPL 2021"),
        html.H2("Description:"),
        html.P("IPL 2021 is being played in India"),
        dcc.RadioItems(
            id="news-class",
            options=[
                {"label": "World News", "value": 1},
                {'label': "Sports", "value": 2},
                {'label': "Business", 'value': 3},
                {'label': "Sci/Tech", 'value': 4},
                {"label": "Not Sure", 'value': 0}
            ], value=0,
            labelStyle={'display': 'block'}
        ),
        html.Div(id="app-2-display-value"),
        dcc.Link(html.Button("Next", id="annotte-next", n_clicks=0), href="/annotate"),
    ]
)
