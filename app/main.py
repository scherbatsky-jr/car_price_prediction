# Import packages
from dash import Dash
import dash_html_components as html
import dash_bootstrap_components as dbc

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout =html.Div([
    html.Link(rel='stylesheet', href='/styles/home.css'),
    html.Div(children=[
        html.Div('Welcome to Sunil Car Center', className="header"),
        html.Div("With our advance AI, you can customize your car and check the possible values", className="message") 
    ]),

    html.Form(children=[
        html.Div([
            dbc.Label("Enter the engine: ", className="inputLabel"),
            dbc.Input(id="engine", type="number", placeholder="Enter the engine")
        ]),

        html.Div([
            dbc.Label("Enter the maxpower: ", className="inputLabel"),
            dbc.Input(id="maxPower", type="number", placeholder="Enter the maxpower")
        ]),

        dbc.Button(id="submit", children="Submit", color="primary")
    ], className="form")
])

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)