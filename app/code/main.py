# Import packages
from dash import Dash, dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import numpy as np
import os 
import pandas as pd
import pickle

# Defining absolute path
absolute_path = os.path.dirname(__file__)

# Loading the model
model_path = os.path.join(absolute_path, '../model/selling-price.model')
loaded_model = pickle.load(open(model_path, "rb"))

# Loading the sclaer
scaler_path = os.path.join(absolute_path, '../model/scaler.pkl')
scaler = pickle.load(open(scaler_path, 'rb'))

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)


# Importing the brand names 
brand_options = [
    'Ambassador', 'Ashok', 'Audi', 'BMW', 'Chevrolet', 'Daewoo',
    'Datsun', 'Fiat', 'Force', 'Ford', 'Honda', 'Hyundai', 'Isuzu',
    'Jaguar', 'Jeep', 'Kia', 'Land', 'Lexus', 'MG', 'Mahindra',
    'Maruti', 'Mercedes-Benz', 'Mitsubishi', 'Nissan', 'Opel',
    'Peugeot', 'Renault', 'Skoda', 'Tata', 'Toyota', 'Volkswagen',
    'Volvo'
]

home_layout = html.Div([
    html.Div(children=[
        html.Div('Welcome to New Car Center', className="header"),
        html.Div("With our advance AI, Get the best price estimation for vehicle of your need!!!!", className="message"),
        html.Div("Please click on the version below you wish to proceed with")
    ]),

    html.Div(children = [
        dcc.Link('V1', className="version-link", href="/v1"),
        dcc.Link('V2', className="version-link", href="/v2")
    ], className="versions"),
])

v1_layout = html.Div([
    html.Div(children=[
        html.Div('Welcome to New Car Center', className="header"),
        html.Div("With our advance AI, Get the best price estimation for vehicle of your need!!!!", className="message"),
    ]),

    html.Div(children=[
        html.Div(
            [
                html.Div(
                    [
                        dbc.Label("Mileage (kmpl)"),
                        dbc.Input(id="mileage-input", type="number", placeholder="Enter the mileage", required=False)

                    ]
                ),

                html.Div(
                    [
                        dbc.Label("Engine (CC)"),
                        dbc.Input(id="engine-input", type="number", placeholder="Enter the engine", required=False)
                    ]
                ),

                html.Div(
                    [
                        dbc.Label("Max Power (bhp)"),
                        dbc.Input(id="max-power-input", type="number", placeholder="Enter the maxpower", required=False)
                    ]
                ),
            ],
            className="form-fields"
        ),

        html.Output(id="error-div", className="error-message"),

        dbc.Button(id="submit-button", children="Submit", color="primary", className="submit"),
    ], className="form"),

    html.Output(id="output-div", className="price-output"),
])

v2_layout = html.Div([
    html.Div(children=[
        html.Div('Welcome to New Car Center', className="header"),
        html.Div("With our advance AI, Get the best price estimation for vehicle of your need!!!!", className="message"),
    ]),

    html.Div(children=[
        html.Div(
            [
                html.Div(
                    [
                        dbc.Label("Mileage (kmpl)"),
                        dbc.Input(id="mileage-input", type="number", placeholder="Enter the mileage", required=False)

                    ]
                ),

                html.Div(
                    [
                        dbc.Label("Engine (CC)"),
                        dbc.Input(id="engine-input", type="number", placeholder="Enter the engine", required=False)
                    ]
                ),

                html.Div(
                    [
                        dbc.Label("Max Power (bhp)"),
                        dbc.Input(id="max-power-input", type="number", placeholder="Enter the maxpower", required=False)
                    ]
                ),
            ],
            className="form-fields"
        ),

        html.Output(id="error-div", className="error-message"),

        dbc.Button(id="submit-button", children="Submit", color="primary", className="submit"),
    ], className="form"),

    html.Output(id="output-div", className="price-output"),
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
    else:
        return home_layout
    
@callback(
    Output("error-div", "children"),
    Output("output-div", "children"),
    Input("submit-button", "n_clicks"),
    State("mileage-input", "value"),
    State("max-power-input", "value"),
    State("engine-input", "value"),
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

    predictions = loaded_model.predict(input)

    predicted_selling_price = "{:,.2f}".format(np.exp(predictions)[0])

    return '', f"Based on your input, the predicted selling price of such car is {predicted_selling_price} Baht"


# App layout
app.layout =html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
], className="layout")

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug = True)