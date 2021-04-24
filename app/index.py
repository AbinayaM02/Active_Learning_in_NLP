import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from layouts import instruction_layout, annotation_layout, initial_layout, annotate_data_dir
import callbacks

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/instruction":
        return instruction_layout
    elif pathname == "/annotate":
        return annotation_layout
    else:
        return initial_layout


if __name__ == "__main__":
    app.run_server(debug=True)