import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
import dash_auth
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from pathlib import Path
import os

import pandas as pd

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
class_map = {1: "World News", 2: "Sports", 3: "Business", 4: "Sci/Tech", 0: "Not Sure"}
annotate_data_dir = Path(__file__).resolve().parents[1] / "annotate_data/20210421"

colors = {"background": "#000000", "text": "#7FDBFF"}
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig.update_layout(
    plot_bgcolor=colors["background"],
    paper_bgcolor=colors["background"],
    font_color=colors["text"],
)


app.layout = html.Div(
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
                                {"label": "Random Sampling", "value": 1},
                                {"label": "Least Confidence Sampling", "value": 2},
                                {"label": "Margin Sampling", "value": 3},
                                {"label": "Entropy Base Sampling", "value": 4},
                            ],
                            style={"width": "50%"},
                        ),
                    ],
                    style={"width": "50%"},
                ),
            ],
            style={"display": "flex", "columnCount": 2},
        ),
        # html.Col(children="check"),
        html.H6("Change Value in the text box to see the callbacks in action"),
        html.Div(
            ["Input:", dcc.Input(id="my-input", value="initial value", type="text")]
        ),
        html.Br(),
        html.Div(
            [
                html.Label("Choose Class"),
                dcc.RadioItems(
                    id="choose-class",
                    options=[
                        {"label": "World News", "value": 1},
                        {"label": "Sports", "value": 2},
                        {"label": "Business", "value": 3},
                        {"label": "Sci/Tech", "value": 4},
                        {"label": "Not Sure", "value": 0},
                    ],
                    value=0,
                ),
            ],
        ),
        html.Div(id="my-output"),
    ],
)


@app.callback(
    Output(component_id="my-output", component_property="children"),
    Input(component_id="choose-class", component_property="value"),
)
def update_output_div(input_value):
    return f"Choosen Class:: {class_map[input_value]}"


@app.callback(Output("choose-data", "options"), Input("choose-data", "search_value"))
def get_data_list(search_value):
    if not search_value:
        raise PreventUpdate
    return [f for f in os.listdir(annotate_data_dir)]


if __name__ == "__main__":
    app.run_server(debug=True)