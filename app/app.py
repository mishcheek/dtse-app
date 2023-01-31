import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from datetime import datetime
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
load_figure_template('LUX')

API_BASE_URL = "http://127.0.0.1:5001" # local
# API_BASE_URL = "http://my_api:8080" # docker

def description_card():
    """ :return: A Div containing dashboard title & description."""
    return html.Div(
        id="description-card",
        children=[
            html.H3("Welcome to the Dash application!"),
            html.H4("House Price Prediction"),
            html.Div(
                id="intro",
                children="Fill in the parameters below to compute the prediction of the house price. Explore average price of previously computed housing predictions in the chart and table on the right.",
            ),
        ],
    )

def input_form():
    """:return: A Div containing form for parameters to be passed to the model upon submission."""
    PROXIMITIES = ['<1H OCEAN', 'INLAND', 'ISLAND', 'NEAR BAY', 'NEAR OCEAN']
    
    return html.Div(
        id="control-card",
        children=[
            dbc.Form([
                dbc.Row([
                    dbc.Col(
                        [
                            dbc.Label("Longitude:"),
                            dbc.Input(
                                type="number",
                                required="True",
                                id="longitude",
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            dbc.Label("Latitude:"),
                            dbc.Input(
                                type="number",
                                required="True",
                                id="latitude",
                            ),
                        ]
                    ),
                ]),
                dbc.Row([
                    dbc.Col(
                        [
                            dbc.Label("Housing median age:"),
                            dbc.Input(
                                type="number",
                                required="True",
                                id="housing_median_age",
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            dbc.Label("Total rooms:"),
                            dbc.Input(
                                type="number",
                                required="True",
                                id="total_rooms",
                            ),
                        ]
                    ),
                ]),
                dbc.Row([
                    dbc.Col(
                        [
                            dbc.Label("Total bedrooms:"),
                            dbc.Input(
                                type="number",
                                required="True",
                                id="total_bedrooms",
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            dbc.Label("Population:"),
                            dbc.Input(
                                type="number",
                                required="True",
                                id="population",
                            ),
                        ]
                    ),
                ]),
                dbc.Row([
                    dbc.Col(
                        [
                            dbc.Label("Households:"),
                            dbc.Input(
                                type="number",
                                required="True",
                                id="households",
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            dbc.Label("Median income:"),
                            dbc.Input(
                                type="number",
                                required="True",
                                id="median_income",
                            ),
                        ]
                    ),
                ]),
                dbc.Label("Select Proximity:"),
                dcc.Dropdown(
                    id="ocean_proximity",
                    options=[{"label": i, "value": i} for i in PROXIMITIES],
                    value=PROXIMITIES[-1],
                ),
                html.Br(),
                html.Div([
                        dbc.Button("Submit",
                            id='submit_button',
                            color="primary",
                            type='submit',
                            className="me-1"
                        ),
                ], className="d-grid gap-2",),
                html.Br()
            ]),
        ],
    )

app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            id="left-column",
            className="four columns",
            children=[
                description_card(),
                input_form(),
                html.Div(id='pred_result')
            ]
        ),
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                dcc.Graph(id='graph'),
                html.Br(),
                dash_table.DataTable(
                    id='table',
                    data=[],
                    columns=[{'name': i, 'id': i} for i in ["time", "prediction"]],
                    page_size=10,
                    style_cell={'padding': '5px','textAlign': 'center'},
                    style_header={'backgroundColor': 'rgb(243, 243, 243)','fontWeight': 'bold'}
                )
            ]
        ),
        dcc.Store(id='prediction_store'),
        dcc.Store(id='table_store', data=[], storage_type='local'),
    ]
)

@app.callback(
    Output('table_store', 'data'),
    Input('prediction_store', 'data'),
    State('table_store', 'data'),
    prevent_initial_call=True
)
def add_row(callback_data, table_data):
    if callback_data is None:
        raise PreventUpdate

    new_row = dict(list(callback_data[0].items())[-2:])

    if not table_data:
        table_data = [new_row]
    else:
        table_data.append(new_row)
    return table_data


@app.callback(
    Output('table', 'data'),
    Output('graph', 'figure'),
    Input('table_store', 'data')
)
def fill_table_and_chart(data):
    if not data:
        raise PreventUpdate

    df = pd.DataFrame(data)
    fig = px.scatter(df, x="time", y="prediction")
    
    if df.size >= 10: # create cumulative mean column line if there's "enough" data
        df['mean']= df['prediction'].expanding().mean()
        fig1 = px.line(df, x='time', y='mean')
        fig1.update_traces(line=dict(color="rgb(239,85,59)"))
        fig = go.Figure(data=fig.data + fig1.data)

    fig.update_layout(
        title={
            'text': 'Average price of housing',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    
    return data[::-1], fig

@app.callback(
    Output("prediction_store", "data"),
    Input('submit_button', 'n_clicks'),
    State('longitude', 'value'),
    State('latitude', 'value'),
    State('housing_median_age', 'value'),
    State('total_rooms', 'value'),
    State('total_bedrooms', 'value'),
    State('population', 'value'),
    State('households', 'value'),
    State('median_income', 'value'),
    State('ocean_proximity', 'value'),
    prevent_initial_call=True
)
def submit_prediction(
    n_clicks,
    longitude,
    latitude,
    housing_median_age,
    total_rooms,
    total_bedrooms,
    population, 
    households, 
    median_income,
    ocean_proximity
):
    if None in list(locals().values())[1:]:  # Prevent callback if the input is incomplete.
        raise PreventUpdate
    
    form_data = locals()
    del form_data['n_clicks'] # Remove unnecessary key-value pair
    response = requests.post(f'{API_BASE_URL}/predict', json=form_data).json()

    if response['status'] == 200:
        data = { 
            'time': str(datetime.now()), 
            'prediction': response['prediction']
        } 

    df = pd.DataFrame([form_data | data])

    return df.to_dict('records')

@app.callback(
    Output('pred_result', 'children'),
    Input('prediction_store', 'data'),
    prevent_initial_call=True
)
def pred_result(data):
    if data is None:
        raise PreventUpdate
    else:        
        return html.Div(
            id='pred_result',
            children=[
                html.H3(f"Predicted house price is ${int(data[0]['prediction'])}")
            ],
        )

if __name__ == '__main__':
    app.run_server(port=5002, debug=True)
    # app.run_server(host="0.0.0.0", port=8081, debug=True)
