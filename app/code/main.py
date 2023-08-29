# Import packages
from dash import Dash, dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import os 
import pickle

# Defining absolute path
absolute_path = os.path.dirname(__file__)

# Loading the model
model_path = os.path.join(absolute_path, '../model/selling-price.model')
loaded_model = pickle.load(open(model_path, "rb"))

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)


# Importing the brand names 
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
        html.Div('Welcome to Advanced Car Center', className="header"),
        html.Div("With our advance AI, you can fill in the fields in the forms below to get the best price estimation for such vehicles.", className="message") 
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

                html.Div(
                    [
                        dbc.Label("Transmission"),
                        dcc.Dropdown(
                            options=[
                                {"label": "Manual", "value": "Manual"},
                                {"label": "Automatic", "value": "Automatic"},
                            ],
                            value=None,
                        ),
                    ]
                ),

                html.Div(
                    [
                        dbc.Label("Mileage"),
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
                        dbc.Label("Max Power"),
                        dbc.Input(id="max-power-input", type="number", placeholder="Enter the maxpower", required=False)
                    ]
                ),

                html.Div(
                    [
                        dbc.Label("Owner"),
                        dcc.Dropdown(
                            options=[
                                {"label": "First Owner", "value": "First Owner"},
                                {"label": "Second Owner", "value": "Second Owner"},
                                {"label": "Third Owner", "value": "Third Owner"},
                            ],
                            value=None,
                        ),
                    ]
                ),

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
    State("max-power-input", "value"),
    prevent_initial_call=True
)
def submit_form(n_clicks, mileage, max_power):
    # mileage = 0 if mileage is None else float(mileage)
    # max_power = 0 if max_power is None else float(max_power)
    # predicted_selling_price = loaded_model.predict(np.array([[float(max_power), float(mileage)]]))

    # predicted_selling_price = "{:,.2f}".format(np.exp(predicted_selling_price)[0])

    return f"Based on your input, the predicted selling price of such car is "


# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug = True)