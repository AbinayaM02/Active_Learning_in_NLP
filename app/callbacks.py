import os
import pandas as pd
import json

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

# Callback for slider
@app.callback(
    Output('slider-output-container', 'children'),
    Input('selected-samples', 'value')
)
def update_output(value):
    return

# Callback for popup
@app.callback(Output('confirm', 'displayed'),
              Input('choose-data', 'value'))
def display_confirm(value):
    if value == None:
        return True
    return False

# Callback for submit
@app.callback(
    [
        Output("selected-data-method", "children"),
        Output("annotate-text", "data"),
    ],
    [
        Input("submit-val", "n_clicks"),
        Input('confirm', 'submit_n_clicks'),
        Input("choose-data", "value"),
        Input("choose-annotate-method", "value"),
        Input("selected-samples", "value"),
    ],
)
def get_data_for_annotation(n_clicks, submit_n_clicks, data, method, sample_size):
    if submit_n_clicks == 0:
        return [True, True]
    if n_clicks:
        data_path = os.path.join(annotate_data_dir, data)
        df_annotate, _ = annotator.get_data(data_path, method, sample_size)
        df_annotate["sampling_method"] = method
        return [True, df_annotate.to_json(orient="columns")]

# Callback for tabs
@app.callback(Output('instruction-example-tab', 'children'),
              Input('tabs-content', 'value'))
def render_content(tab):
    if tab == 'Annotation Instructions':
        return instruction_tab_content
    elif tab == 'Annotation Examples':
        return example_tab_content

# Callback for annotation_layout
@app.callback(
    [
        Output("title-body", "children"), 
        Output("description-body", "children"),  
    ],
    [
        Input("annotate-next", "n_clicks"),
        Input("annotate-prev", "n_clicks"),
        Input("news-class", 'value')
    ],
    State("annotate-text", "data")
)
def sample_data(n_clicks_next, n_clicks_back, news_type, df_json):
    df = pd.DataFrame.from_dict(json.loads(df_json))
    print(n_clicks_next)
    if n_clicks_back == 0 and n_clicks_next == 0:
        df_index = df["idx"].values[0]
        title = df["text"].values[0]
        description = df["title"].values[0]
    if n_clicks_next:
        df_index = df["idx"].values[n_clicks_next]
        title = df["text"].values[n_clicks_next]
        description = df["title"].values[n_clicks_next]
    elif n_clicks_back:
        df_index = df["idx"].values[n_clicks_next - 1]
        title = df["text"].values[n_clicks_next - 1]
        description = df["title"].values[n_clicks_next - 1]
    df.loc[df["idx"] == df_index, "annotated_labels"]= news_type - 1
    print(df)
    return [f"Title:\n {title}", f"Description:\n {description}"]

