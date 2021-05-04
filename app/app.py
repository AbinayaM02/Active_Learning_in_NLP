import dash
import dash_bootstrap_components as dbc

# Define the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI], suppress_callback_exceptions=True)
server = app.server
