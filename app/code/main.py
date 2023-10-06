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

from pages.v1 import v1_layout
from pages.v2 import v2_layout
from pages.v3 import v3_layout

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
def submit_v1_form(n_clicks, mileage, max_power, engine):
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
def submit_v2_form(n_clicks, mileage, max_power, engine):
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
def submit_v3_form(n_clicks, mileage, max_power, engine):
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

    return '', f"Based on your input, the predicted selling price category is of such car is {predictions[0]}"

# App layout
app.layout =html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
], className="layout")

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=80, debug = True)