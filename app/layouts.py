import os
from pathlib import Path

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

colors = {"background": "#000000", "text": "#7FDBFF"}
class_map = {1: "World News", 2: "Sports", 3: "Business", 4: "Sci/Tech", 0: "Not Sure"}
annotate_data_dir = Path(__file__).resolve().parents[1] / "data/output/20210421"

data_file_dropdown = dcc.Dropdown(
    id="choose-data",
    options=[{"label": i, "value": i} for i in os.listdir(annotate_data_dir)],
    style={"width": "75%"},
)

annotation_method_dropdown = dcc.Dropdown(
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
    value="random",
    style={"width": "75%"},
)

sample_slider = dcc.Slider(
    id="selected-samples",
    min=0,
    max=1000,
    step=10,
    marks={i: "{}".format(i) for i in range(1001) if i % 100 == 0},
    value=50,
    updatemode="drag",
    tooltip={"always_visible": False},
)

popup_layout = html.Div(
    [
        dcc.ConfirmDialog(
            id="confirm",
            message="No file is chosen! Do you want to continue?",
        ),
        html.Div(id="output-confirm"),
    ]
)

tagging_layout = html.Div(
    [
        dbc.CardHeader(
            children="annotate.it",
            style={"textAlign": "center"},
        ),
        popup_layout,
        dbc.Card(
            [
                html.Div(
                    [
                        html.Br(),
                        html.Br(),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.FormGroup(
                                [dbc.Label("Choose data to annotate"), data_file_dropdown]
                            ),
                            width={"size": 5, "order": "first", "offset": 1},
                        ),
                        dbc.Col(
                            dbc.FormGroup(
                                [dbc.Label("Choose annotation method"), annotation_method_dropdown]
                            ),
                            width={"size": 5, "order": "last", "offset": 1},
                        ),
                    ],
                    justify="around",
                ),
                html.Div(
                    [
                        html.Br(),
                        html.Br(),
                        dbc.Label("Select number of samples"),
                        sample_slider,
                        html.Div(id="slider-output-container"),
                    ]
                ),
                html.Div(
                    [
                        html.Br(),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button(
                                        "Submit",
                                        id="submit-val",
                                        n_clicks=0,
                                        color="primary",
                                        size="md",
                                        className="mt-auto",
                                        href="/annotate",
                                    ),
                                    width=4,
                                ),
                            ],
                            justify="around",
                        ),
                    ],
                    style={"textAlign": "center", "margin": "auto"},
                ),
            ]
        ),
        html.H1(id="selected-data-method"),
    ],
    className="m-4 px-2",
)

instruction_tab_content = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.P(
                    """In this exercise we will be labeling news into one of the below four categories.
                In case, news is ambigous, please choose option `Not Sure`"""
                ),
                html.Ol(
                    [
                        html.Li(html.B("World News")),
                        html.Li(html.B("Sports")),
                        html.Li(html.B("Business")),
                        html.Li(html.B("Sci/Tech")),
                        html.Li(html.B("Not sure")),
                    ]
                ),
            ],
            className="mt-3",
        ),
    ],
)

example_tab_content = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.P("""Examples for each of the categories are shown below:"""),
                html.Ol(
                    [
                        html.Li(html.B("World News")),
                        html.B("Title: "),
                        html.P(""" White House Proposes Cuts in Salmon Areas (AP) """),
                        html.B("Description: "),
                        html.P(
                            """
                            AP - The Bush administration Tuesday proposed large cuts in
                            federally designated areas in the Northwest and California meant
                            to aid the recovery of threatened or endangered salmon.
                            Protection would focus instead on rivers where the fish now thrive.
                            """
                        ),
                        html.Li(html.B("Sports News")),
                        html.B("Title: "),
                        html.P(""" Wannstedt Steps Down as Dolphins Coach """),
                        html.B("Description: "),
                        html.P(
                            """
                            DAVIE, Fla. (Sports Network) - Dave Wannstedt resigned  Tuesday as head
                            coach of the Miami Dolphins after the team sunk  to an NFL-worst 1-8 record.
                            Defensive coordinator Jim Bates  will take over as interim coach for
                            the remainder of the  season.
                            """
                        ),
                        html.Li(html.B("Business News")),
                        html.B("Title: "),
                        html.P(""" Credit Issuers Shares Dented by Kerry Plan """),
                        html.B("Description: "),
                        html.P(
                            """
                            Financial companies were under scrutiny Friday after Sen.
                            John Kerry vowed to push for legislation that would curb credit card fees
                            and protect homebuyers from unfair lending practices.
                            """
                        ),
                        html.Li(html.B("Sci/Tech News")),
                        html.B("Title: "),
                        html.P(""" Titan on Tuesday """),
                        html.B("Description: "),
                        html.P(
                            """
                            On Tuesday, October 26, the Cassini spacecraft will approach Saturn #39;s
                            largest moon, Titan. Cassini will fly by Titan at a distance of 1,200 kilometers
                            (745 miles) above the surface, nearly 300 times closer than the first Cassini
                            flyby of Titan on July 3.
                            """
                        ),
                    ]
                ),
            ],
            className="mt-3",
        ),
    ]
)

instruction_example_tabs = html.Div(
    [
        dbc.CardHeader(
            children="Annotation Instructions and Examples",
            style={"textAlign": "center"},
        ),
        dbc.Tabs(
            [
                dbc.Tab(
                    instruction_tab_content,
                    label="Annotation Instructions",
                    tab_id="tab-instruction",
                ),
                dbc.Tab(example_tab_content, label="Annotation Examples", tab_id="tab-example"),
            ],
            id="tabs-content",
        ),
        html.Div(id="instruction-example-tab"),
    ]
)

annotation_layout = html.Div(
    [
        dbc.CardHeader(
            children="Annotate.it",
            style={"textAlign": "center"},
        ),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H5("Title:\n", className="card-title"),
                        html.P("IPL 2021 is being played in India"),
                    ],
                    id="title-body",
                ),
                dbc.CardBody(
                    [
                        html.H5("Description:\n", className="card-title"),
                        html.P("IPL 2021 is being played in India"),
                    ],
                    id="description-body",
                ),
                dbc.CardBody(
                    [
                        dbc.Label(
                            "Please choose one of the five categories that describes the text well!",
                            align="start",
                            size="md",
                        ),
                        dbc.RadioItems(
                            id="news-class",
                            options=[
                                {"label": "World News", "value": 1},
                                {"label": "Sports", "value": 2},
                                {"label": "Business", "value": 3},
                                {"label": "Sci/Tech", "value": 4},
                                {"label": "Not Sure", "value": 0},
                            ],
                            value=0,
                            inline=True,
                            style={"textAlign": "center"},
                        ),
                    ]
                ),
                html.Div(id="annotate-data"),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Div(
                    [
                        dcc.Link(
                            dbc.Button(
                                "Back", id="annotate-prev", n_clicks=0, color="secondary", size="md"
                            ),
                            href="/annotate",
                        ),
                        dcc.Link(
                            dbc.Button(
                                "Save", id="save-link", n_clicks=0, color="primary", size="md"
                            ),
                            href="/annotate",
                        ),
                        dcc.Link(
                            dbc.Button(
                                "Next", id="annotate-next", n_clicks=0, color="secondary", size="md"
                            ),
                            href="/annotate",
                        ),
                    ],
                    style={"textAlign": "center"},
                ),
            ],
        ),
    ]
)

stat_layout = html.Div(
    [
        dbc.CardHeader(
            children="Annotate.it : Statistics",
            style={"textAlign": "center"},
        ),
        dbc.Card([dbc.CardBody([dcc.Graph(id="stat-graph")])]),
    ],
    id="stat-container",
)

report_layout = html.Div(
    [
        dbc.CardHeader("Active learning in NLP", style={"textAlign": "center"}),
        dbc.CardBody(
            html.Iframe(
                src=os.path.join("assets", "sample.pdf"),
                style={"width": "910px", "height": "700px"},
            ),
        ),
    ]
)
# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H4("Active Learning", className="display-6"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/home", active="exact"),
                dbc.NavLink("Annotate", href="/annotate_info", active="exact"),
                dbc.NavLink("Annotation Statistics", href="/annotate-stat", active="exact"),
                dbc.NavLink("Project Report", href="/report", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

sidebar_content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)
