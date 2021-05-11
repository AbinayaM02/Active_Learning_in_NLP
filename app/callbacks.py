import os
from dash_html_components.Title import Title
import pandas as pd
import json

# import pandas as pd
from dash.dependencies import Input, Output, State
from layouts import (
    annotate_data_dir,
    annotation_layout,
    instruction_example_tabs,
    # instruction_layout,
    example_layout,
    tagging_layout,
)
from scripts import annotator
from app import app


@app.callback(Output("slider-output-container", "children"), Input("selected-samples", "value"))
def update_output(value):
    return 'You have selected "{}" samples to annotate'.format(value)


@app.callback(
    [Output("selected-data-method", "children"), Output("annotate-text", "data")],
    Input("submit-val", "n_clicks"),
    [
        State("choose-data", "value"),
        State("choose-annotate-method", "value"),
        State("selected-samples", "value"),
    ],
)
def get_data_for_annotation(n_clicks, data, method, sample_size):
    if n_clicks == 0:
        return "No Data Selected", pd.DataFrame().to_json(date_format="iso", orient="split")
    data_path = os.path.join(annotate_data_dir, data)

    df = annotator.get_data(data_path, method, sample_size)
    # global df_annotate
    df_annotate = df[0]
    # print(df_annotate.head())

    return (
        f"Data is {data}, annotation method {method}",
        df_annotate.to_json(orient="columns"),
    )


@app.callback(Output("instruction-example-tab", "children"), Input("tabs-content", "value"))
def render_content(tab):
    if tab == "Annotation Instructions":
        return instruction_layout
    elif tab == "Annotation Examples":
        return example_layout


@app.callback(
    [Output("title", "children"), Output("description", "children")],
    [Input("annotate-next", "n_clicks"), Input("annotate-text", "data")],
    State("news-class", 'value')
)
def sample_data(n_clicks, df_json):
    # if n_clicks == 0:
    df = pd.DataFrame.from_dict(json.loads(df_json))
    title = df["title"].values[n_clicks]
    description = df["description"].values[n_clicks]
    # print(title)
    return [f"Title: {title}", f"Descripton: {description}"]

@app.callback([])