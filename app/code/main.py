# Import packages
from dash import Dash, dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import numpy as np
import os 
import pandas as pd
import pickle
from lib.lasso import Lasso, LassoPenalty
from lib.ridge import Ridge, RidgePenalty

# Defining absolute path
absolute_path = os.path.dirname(__file__)

# Loading the model for version 1
model_path = os.path.join(absolute_path, '../model/selling-price.model')
v1_model = pickle.load(open(model_path, "rb"))

# Loading the model for version 2
v2_model_path = os.path.join(absolute_path, '../model/v2-model.pkl')
v2_model = pickle.load(open(v2_model_path, "rb"))

# Loading the model for version 3
v3_model_path = os.path.join(absolute_path, '../model/v3-model.pkl')
v3_model = pickle.load(open(v3_model_path, "rb"))

# Loading the sclaer
scaler_path = os.path.join(absolute_path, '../model/scaler.pkl')
scaler = pickle.load(open(scaler_path, 'rb'))

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

home_layout = html.Div([
    html.Div(children=[
        html.Div('Welcome to New Car Center', className="header"),
        html.Div("With our advance AI, Get the best price estimation for vehicle of your need!!!!", className="message"),
        html.Div("Please click on the version below you wish to proceed with")
    ]),

    html.Div(children = [
        dcc.Link('V1', className="version-link", href="/v1"),
        dcc.Link('V2', className="version-link", href="/v2"),
        dcc.Link('V3', className="version-link", href="/v3")
    ], className="versions"),
])

v1_layout = html.Div([
    dcc.Link('Back to home page', href="/"),
    html.Div(children=[
        html.Div('You are predicting using Version 1 model!!!!!', className="header"),
        html.Div("With our advance AI, Get the best price estimation for vehicle of your need!!!!", className="message"),
    ]),

    html.Div(children=[
        html.Div(
            [
                html.Div(
                    [
                        dbc.Label("Mileage (kmpl)"),
                        dbc.Input(id="mileage-input-1", type="number", placeholder="Enter the mileage", required=False)

                    ]
                ),

                html.Div(
                    [
                        dbc.Label("Engine (CC)"),
                        dbc.Input(id="engine-input-1", type="number", placeholder="Enter the engine", required=False)
                    ]
                ),

                html.Div(
                    [
                        dbc.Label("Max Power (bhp)"),
                        dbc.Input(id="max-power-input-1", type="number", placeholder="Enter the maxpower", required=False)
                    ]
                ),
            ],
            className="form-fields"
        ),

        html.Output(id="error-div-1", className="error-message"),

        dbc.Button(id="submit-button-1", children="Submit", color="primary", className="submit"),
    ], className="form"),

    html.Output(id="output-div-1", className="price-output"),
])

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

v3_layout = html.Div([
    html.Div(children=[
        dcc.Link('Back to home page', href="/"),
        html.Div('Get better with our updated version 3 model !!!!', className="header"),
        html.Div("With our advance AI, Get the best price estimation for vehicle of your need!!!!", className="message"),
    ]),

    html.Div(children=[
        html.Div(
            [
                html.Div(
                    [
                        dbc.Label("Mileage (kmpl)"),
                        dbc.Input(id="mileage-input-3", type="number", placeholder="Enter the mileage", required=False)

                    ]
                ),

                html.Div(
                    [
                        dbc.Label("Engine (CC)"),
                        dbc.Input(id="engine-input-3", type="number", placeholder="Enter the engine", required=False)
                    ]
                ),

                html.Div(
                    [
                        dbc.Label("Max Power (bhp)"),
                        dbc.Input(id="max-power-input-3", type="number", placeholder="Enter the maxpower", required=False)
                    ]
                ),
            ],
            className="form-fields"
        ),

        html.Output(id="error-div-3", className="error-message"),

        dbc.Button(id="submit-button-3", children="Submit", color="primary", className="submit"),
    ], className="form"),

    html.Output(id="output-div-3", className="price-output"),
])

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/v1':
        return v1_layout
    elif pathname == '/v2':
        return v2_layout
    elif pathname == '/v3':
        return v3_layout
    else:
        return home_layout
    
@callback(
    Output("error-div-1", "children"),
    Output("output-div-1", "children"),
    Input("submit-button-1", "n_clicks"),
    State("mileage-input-1", "value"),
    State("max-power-input-1", "value"),
    State("engine-input-1", "value"),
    prevent_initial_call=True
)
def submit_form(n_clicks, mileage, max_power, engine):
    if mileage is None or max_power is None or engine is None:
        return f"All fields are required.", ' '

    input = pd.DataFrame({
        'max_power': [max_power],
        'engine': [engine],
        'mileage': [mileage]
    })

    input = scaler.transform(input)

    predictions = v1_model.predict(input)

    predicted_selling_price = "{:,.2f}".format(np.exp(predictions)[0])

    return '', f"Based on your input, the predicted selling price of such car is {predicted_selling_price} Baht"


@callback(
    Output("error-div-2", "children"),
    Output("output-div-2", "children"),
    Input("submit-button-2", "n_clicks"),
    State("mileage-input-2", "value"),
    State("max-power-input-2", "value"),
    State("engine-input-2", "value"),
    prevent_initial_call=True
)
def submit_form(n_clicks, mileage, max_power, engine):
    if mileage is None or max_power is None or engine is None:
        return f"All fields are required.", ' '

    input = pd.DataFrame({
        'max_power': [max_power],
        'engine': [engine],
        'mileage': [mileage]
    })

    input = scaler.transform(input)

    intercept = np.ones((input.shape[0], 1))

    input = np.concatenate((intercept, input), axis = 1)

    predictions = v2_model.predict(input)

    predicted_selling_price = "{:,.2f}".format(np.exp(predictions)[0])

    return '', f"Based on your input, the predicted selling price of such car is {predicted_selling_price} Baht"

@callback(
    Output("error-div-3", "children"),
    Output("output-div-3", "children"),
    Input("submit-button-3", "n_clicks"),
    State("mileage-input-3", "value"),
    State("max-power-input-3", "value"),
    State("engine-input-3", "value"),
    prevent_initial_call=True
)
def submit_form(n_clicks, mileage, max_power, engine):
    if mileage is None or max_power is None or engine is None:
        return f"All fields are required.", ' '

    input = pd.DataFrame({
        'max_power': [max_power],
        'engine': [engine],
        'mileage': [mileage]
    })

    input = scaler.transform(input)

    intercept = np.ones((input.shape[0], 1))

    input = np.concatenate((intercept, input), axis = 1)

    predictions = v3_model.predict(input)

    return '', f"Based on your input, the predicted selling price category of such car is {predictions[0]}"

# App layout
app.layout =html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
], className="layout")

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=80, debug = True)