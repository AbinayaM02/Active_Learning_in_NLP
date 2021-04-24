import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from layouts import initial_layout, layout1, layout2  # annotate_data_dir

from app import app

# import callbacks

app.layout = html.Div([dcc.Location(id="url", refresh=False), html.Div(id="page-content")])


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/apps/app1":
        return layout1
    elif pathname == "/apps/app2":
        return layout2
    else:
        return initial_layout


if __name__ == "__main__":
    app.run_server(debug=True)
