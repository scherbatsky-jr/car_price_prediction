# Import packages
from dash import Dash, dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pickle
import numpy as np

loaded_model = pickle.load(open("./model/selling-price.model", "rb"))

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

brand_options = [
    'Ambassador', 'Ashok', 'Audi', 'BMW', 'Chevrolet', 'Daewoo',
    'Datsun', 'Fiat', 'Force', 'Ford', 'Honda', 'Hyundai', 'Isuzu',
    'Jaguar', 'Jeep', 'Kia', 'Land', 'Lexus', 'MG', 'Mahindra',
    'Maruti', 'Mercedes-Benz', 'Mitsubishi', 'Nissan', 'Opel',
    'Peugeot', 'Renault', 'Skoda', 'Tata', 'Toyota', 'Volkswagen',
    'Volvo'
]

# App layout
app.layout =html.Div([
    html.Div(children=[
        html.Div('Welcome to New Car Center', className="header"),
        html.Div("With our advance AI, you can customize your car and check the possible value", className="message") 
    ]),

    html.Div(children=[
        html.Div(
            [
                html.Div(
                    [
                        dbc.Label("Brand"),
                        dcc.Dropdown(
                            id="brand-input",
                            options=[{"label": brand, "value": brand} for brand in brand_options],
                            value=None,
                        ),
                    ]
                ),

                html.Div(
                    [
                        dbc.Label("Year"),
                        dcc.Dropdown(
                            id="year-input",
                            options=[
                                {"label": str(year), "value": year}
                                for year in range(1970, 2024)
                            ],
                            value=None,
                        ),
                    ]
                ),

                html.Div(
                    [
                        dbc.Label("Fuel Type"),
                        dcc.Dropdown(
                            options=[
                                {"label": "Diesel", "value": "Diesel"},
                                {"label": "Petrol", "value": "Petrol"},
                            ],
                            value=None,
                        ),
                    ]
                ),

                html.Div(
                    [
                        dbc.Label("Kilometre Driven"),
                        dbc.Input(type="number", value=None),
                    ]
                ),

                html.Div([
                   dbc.Label("Transmission"),
                    dcc.Dropdown(
                        options=[
                            {"label": "Manual", "value": "Manual"},
                            {"label": "Automatic", "value": "Automatic"},
                        ],
                        value=None,
                    ),
                ]),

                html.Div([
                    dbc.Label("Mileage"),
                    dbc.Input(id="mileage-input", type="number", placeholder="Enter the mileage")
                ]),

                html.Div([
                    dbc.Label("Engine (CC)"),
                    dbc.Input(id="engine-input", type="number", placeholder="Enter the engine")
                ]),

                html.Div([
                    dbc.Label("Max Power"),
                    dbc.Input(id="max-power-input", type="number", placeholder="Enter the maxpower")
                ]),

                html.Div([
                    dbc.Label("Owner"),
                    dcc.Dropdown(
                        options=[
                            {"label": "First Owner", "value": "First Owner"},
                            {"label": "Second Owner", "value": "Second Owner"},
                            {"label": "Third Owner", "value": "Third Owner"},
                        ],
                        value=None,
                    ),
                ]),

                html.Div(
                    [
                        dbc.Label("Torque"),
                        dbc.Input(type="number", value=None),
                    ]
                ),
                html.Div(
                    [
                        dbc.Label("Seats"),
                        dbc.Input(type="number", value=None),
                    ]
                ),
            ],
            className="form-fields"
        ),

        dbc.Button(id="submit-button", children="Submit", color="primary", className="submit"),
    ], className="form"),

    html.Output(id="output-div", className="price-output"),
], className="layout")

@callback(
    Output("output-div", "children"),
    Input("submit-button", "n_clicks"),
    State("mileage-input", "value"),
    State("engine-input", "value"),
    State("max-power-input", "value"),
    prevent_initial_call=True
    # State("max-power-input", "value"),
    # Add other input components here
)
def submit_form(n_clicks, mileage, engine, max_power):
    predicted_selling_price = loaded_model.predict(np.array([[engine, max_power, mileage]]))

    predicted_selling_price = "{:,.2f}".format(np.exp(predicted_selling_price)[0])

    return f"Based on your input, the predicted selling price of such car is {predicted_selling_price}"
    

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug = True)