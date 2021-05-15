import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from layouts import (
    annotation_layout,
    instruction_example_tabs,
    report_layout,
    sidebar,
    sidebar_content,
    stat_layout,
    tagging_layout,
)
import callbacks
from app import app

# Define app layout
app.layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        # html.Div(id="page-content")
        sidebar,
        sidebar_content,
        dcc.Store(id="annotate-text", storage_type="local"),
    ],
    fluid=True,
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/home":
        return instruction_example_tabs
    elif pathname == "/annotate":
        return annotation_layout
    elif pathname == "/annotate_info":
        return tagging_layout
    elif pathname == "/annotate-stat":
        return stat_layout
    elif pathname == "/report":
        return report_layout
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(
        debug=True,
    )
