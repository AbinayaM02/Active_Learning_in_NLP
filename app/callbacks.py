import os

# import pandas as pd
from dash.dependencies import Input, Output, State
from layouts import (annotate_data_dir,
                    annotation_layout,
                    instruction_example_tabs,
                    instruction_tab_content,
                    example_tab_content,
                    tagging_layout)
from scripts import annotator
from app import app

@app.callback(
    Output('slider-output-container', 'children'),
    Input('selected-samples', 'value')
)
def update_output(value):
    return 'You have selected "{}" samples to annotate'.format(value)

@app.callback(
    Output("selected-data-method", "children"),
    Input("submit-val", "n_clicks"),
    [
        State("choose-data", "value"),
        State("choose-annotate-method", "value"),
        State("selected-samples", "value"),
    ],
)
def get_data_for_annotation(n_clicks, data, method, sample_size):
    if n_clicks == 0:
        return "No Data Selected"
    data_path = os.path.join(annotate_data_dir, data)
    df_annotate, df_annotated = annotator.get_data(data_path, method, sample_size)
    print(df_annotate.head())

    return f"Data is {data}, annotation method {method}"


@app.callback(Output('instruction-example-tab', 'children'),
              Input('tabs-content', 'value'))
def render_content(tab):
    if tab == 'Annotation Instructions':
        return instruction_tab_content
    elif tab == 'Annotation Examples':
        return example_tab_content


