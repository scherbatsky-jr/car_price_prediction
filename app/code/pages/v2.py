# Import packages
from dash import dcc, html
import dash_bootstrap_components as dbc

v2_layout = html.Div([
    html.Div(children=[
        dcc.Link('Back to home page', href="/"),
        html.Div('Get better with our updated version 2 model !!!!', className="header"),
        html.Div("With our advance AI, Get the best price estimation for vehicle of your need!!!!", className="message"),
    ]),

    html.Div(children=[
        html.Div(
            [
                html.Div(
                    [
                        dbc.Label("Mileage (kmpl)"),
                        dbc.Input(id="mileage-input-2", type="number", placeholder="Enter the mileage", required=False)

                    ]
                ),

                html.Div(
                    [
                        dbc.Label("Engine (CC)"),
                        dbc.Input(id="engine-input-2", type="number", placeholder="Enter the engine", required=False)
                    ]
                ),

                html.Div(
                    [
                        dbc.Label("Max Power (bhp)"),
                        dbc.Input(id="max-power-input-2", type="number", placeholder="Enter the maxpower", required=False)
                    ]
                ),
            ],
            className="form-fields"
        ),

        html.Output(id="error-div-2", className="error-message"),

        dbc.Button(id="submit-button-2", children="Submit", color="primary", className="submit"),
    ], className="form"),

    html.Output(id="output-div-2", className="price-output"),
])
