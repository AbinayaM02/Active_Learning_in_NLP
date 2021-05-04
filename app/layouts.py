import os
from pathlib import Path
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html


colors = {"background": "#000000", "text": "#7FDBFF"}
class_map = {1: "World News", 2: "Sports", 3: "Business", 4: "Sci/Tech", 0: "Not Sure"}
annotate_data_dir = Path(__file__).resolve().parents[1] / "data/output/20210421"

tagging_layout = html.Div(
    children=[
        html.H1(
            children="annotate.it",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        html.Div(
            [
                html.Label(
                    [
                        "Choose data to annotate",
                        dcc.Dropdown(
                            id="choose-data",
                            options=[
                                {"label": i, "value": i} for i in os.listdir(annotate_data_dir)
                            ],
                            style={"width": "75%"},
                        ),
                    ],
                    style={"width": "50%"},
                ),
                html.Label(
                    [
                        "Choose annotation method",
                        dcc.Dropdown(
                            id="choose-annotate-method",
                            options=[
                                {"label": "Random Sampling", "value": "random"},
                                {"label": "Least Confidence Sampling", "value": "least",},
                                {"label": "Margin Sampling", "value": "margin"},
                                {"label": "Entropy Base Sampling", "value": "entropy"},
                            ],
                            value="random",
                            style={"width": "75%"},
                        ),
                    ],
                    style={"width": "50%"},
                ),
            ],
            style={"display": "flex", "columnCount": 2, "padding": 50},
        ),
        html.Div(
            [
                html.Label('Select number of samples'),
                dcc.Slider(
                    id='selected-samples',
                    min=0,
                    max=1000,
                    step=10,
                    marks={i: '{}'.format(i) for i in range(1001) if i%100 == 0},
                    value=50,
                    updatemode='drag',
                ),
                html.Div(id='slider-output-container', style={"padding": 30}),
            ],
        ),
        dcc.Link(
            html.Button(children="Submit", id="submit-val", n_clicks=0),
            href="/annotate",
        ),
        html.H1(id="selected-data-method"),
    ]
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

example_tab_content  = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.P(
                    """Examples for each of the categories are shown below:"""
                ),
                html.Ol(
                    [
                        html.Li(html.B("World News")),
                        html.B("Title: "),
                        html.P( 
                            """ White House Proposes Cuts in Salmon Areas (AP) """
                        ),
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
                        html.P( 
                            """ Wannstedt Steps Down as Dolphins Coach """
                        ),
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
                        html.P( 
                            """ Credit Issuers Shares Dented by Kerry Plan """
                        ),
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
                        html.P( 
                            """ Titan on Tuesday """
                        ),
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
        html.H2(
            children="Annotation Instructions and Examples",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        dbc.Tabs(
            [
                dbc.Tab(instruction_tab_content, label="Annotation Instructions", tab_id="tab-instruction"),
                dbc.Tab(example_tab_content, label="Annotation Examples", tab_id="tab-example"),
            ],
            id="tabs-content",
        ),
        html.Div(id='instruction-example-tab'),
        dcc.Link(
            dbc.Button(children="Next", id="annotate-val", n_clicks=0, color="primary"),
            href="/annotate_info",
        ),
    ]
)

annotation_layout = html.Div(
    [
        html.H4("Title:"),
        html.H4(
            id="title",
        ),
        html.P("IPL 2021"),
        html.H4("Description:"),
        html.P("IPL 2021 is being played in India"),
        dcc.RadioItems(
            id="news-class",
            options=[
                {"label": "World News", "value": 1},
                {"label": "Sports", "value": 2},
                {"label": "Business", "value": 3},
                {"label": "Sci/Tech", "value": 4},
                {"label": "Not Sure", "value": 0},
            ],
            value=0,
            labelStyle={"display": "block"},
        ),
        html.Div(id="annotate-data"),
        html.Div(
            [
                dcc.Link(html.Button("Home", id="home-link", n_clicks=0), href="/home"),
                dcc.Link(html.Button("Next", id="annotate-next", n_clicks=0), href="/annotate"),
            ],
            style={"textAlign": 'center'}
        ),
    ]
)
