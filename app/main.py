# Import packages
from dash import Dash, html, callback, Output, Input, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout =html.Div([
    html.Div(children=[
        html.H1('Welcome to Chakky Car Center'),
        html.H2("With our advance AI, you can customize your car and check the possible values") 
    ]),

    html.Form(children=[
        html.Div([
            dbc.Label("Enter the engine: "),
            dbc.Input(id="engine", type="number", placeholder="Enter the engine")
        ]),

        html.Div([
            dbc.Label("Enter the maxpower: "),
            dbc.Input(id="maxPower", type="number", placeholder="Enter the maxpower")
        ]),

        dbc.Button(id="submit", children="Submit", color="primary")
    ])
])

@callback(
    Output(component_id="y", component_property="children"),
    State(component_id="x_1", component_property="value"),
    State(component_id="x_2", component_property="value"),
    Input(component_id="submit", component_property='n_clicks'),
    prevent_initial_call=True
)

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)