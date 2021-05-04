import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app
from layouts import (  # annotate_data_dir
    annotation_layout,
    tagging_layout,
    instruction_example_tabs
)
import callbacks

# Define app layout
app.layout = html.Div(children=[
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])


@app.callback(
    Output("page-content", "children"), 
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/home":
        return instruction_example_tabs
    elif pathname == "/annotate":
        return annotation_layout
    elif pathname == "/annotate_info":
        return tagging_layout
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == "__main__":
    app.run_server(debug=True, )
