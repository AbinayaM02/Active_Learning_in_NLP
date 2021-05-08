import os
import pandas as pd

# import pandas as pd
from dash.dependencies import Input, Output, State
from layouts import (annotate_data_dir,
                    annotation_layout,
                    instruction_example_tabs,
                    instruction_tab_content,
                    example_tab_content,
                    tagging_layout,
                    popup_layout,
                    stat_layout)
from scripts import annotator
from app import app

data = pd.read_csv("https://cdn.opensource.faculty.ai/world-phones/data.csv")

# Callback for slider
@app.callback(
    Output('slider-output-container', 'children'),
    Input('selected-samples', 'value')
)
def update_output(value):
    return 'You have selected "{}" samples to annotate'.format(value)

# Callback for popup
@app.callback(Output('confirm', 'displayed'),
              Input('choose-data', 'value'))
def display_confirm(value):
    if value == None:
        return True
    return False

# Callback for submit
@app.callback(
    Output("selected-data-method", "children"),
    [
        Input("submit-val", "n_clicks"),
        Input('confirm', 'submit_n_clicks'),
        Input("choose-data", "value"),
        Input("choose-annotate-method", "value"),
        Input("selected-samples", "value"),
    ],
    # [
    #     State("choose-data", "value"),
    #     State("choose-annotate-method", "value"),
    #     State("selected-samples", "value"),
    # ],
)
def get_data_for_annotation(n_clicks, submit_n_clicks, data, method, sample_size):
    if n_clicks:
        return popup_layout
    if submit_n_clicks:
        data_path = os.path.join(annotate_data_dir, data)
        df_annotate, df_annotated = annotator.get_data(data_path, method, sample_size)
        return True

# Callback for tabs
@app.callback(Output('instruction-example-tab', 'children'),
              Input('tabs-content', 'value'))
def render_content(tab):
    if tab == 'Annotation Instructions':
        return instruction_tab_content
    elif tab == 'Annotation Examples':
        return example_tab_content


