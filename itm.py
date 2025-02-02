import math
import os
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go
import pandas as pd
import random
import datetime
from flask import Flask, send_file, render_template_string
from scipy.stats import norm

# Initialize Flask and Dash apps
server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Initial prices for different strikes
strikes = [23000, 24000, 25000, 26000, 27000]
prices = {strike: {'call': 200, 'put': 200, 'straddle': []} for strike in strikes}

# Data storage for time series
time_series = [datetime.datetime.now()]

# List of random stock names
stock_names = ['RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK', 'KOTAKBANK', 'SBIN', 'BAJFINANCE', 'HINDUNILVR', 'ITC']

# Static list of strike prices for option chain
option_strike_prices = [23000, 23050, 23100]

# Function to generate random stock prices
def generate_stock_data():
    return pd.DataFrame({
        'Stock Name': stock_names,
        'Price': [round(random.uniform(1000, 3000), 2) for _ in stock_names]
    })

# Function to generate random option chain data
def generate_option_chain_data():
    data = []
    for strike in option_strike_prices:
        data.append({
            'Call OI': random.randint(1000, 5000),
            'Call ChangeInOI': random.randint(-500, 500),
            'Call Price': round(random.uniform(100, 300), 2),
            'Strike Price': strike,
            'Put OI': random.randint(1000, 5000),
            'Put ChangeInOI': random.randint(-500, 500),
            'Put Price': round(random.uniform(100, 300), 2)
        })
    return pd.DataFrame(data)

# Function to generate random India VIX value
def generate_india_vix():
    return round(random.uniform(12.0, 18.0), 2)

# Function to calculate ITM probability
def calculate_itm_probability(S, K, T, r, sigma, option_type='call'):
    if T == 0:
        if option_type == 'call':
            return 100 if S >= K else 0
        elif option_type == 'put':
            return 100 if S <= K else 0
        else:
            raise ValueError("Invalid option type. Use 'call' or 'put'.")
    d2 = (math.log(S / K) + (r - 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    if option_type == 'call':
        return norm.cdf(d2) * 100
    elif option_type == 'put':
        return (1 - norm.cdf(d2)) * 100

# Function to generate ITM probability data
def generate_itm_data():
    S = 23100
    r = 0.03
    sigma = 0.2
    strike_prices = range(22000, 24001, 500)
    days_in_month = 30

    data = []
    for K in strike_prices:
        for day in range(days_in_month + 1):
            T = (days_in_month - day) / 365
            call_prob = calculate_itm_probability(S, K, T, r, sigma, 'call')
            put_prob = calculate_itm_probability(S, K, T, r, sigma, 'put')
            data.append({'Strike Price': K, 'Day': day, 'Call ITM %': round(call_prob, 2), 'Put ITM %': round(put_prob, 2)})

    return pd.DataFrame(data)

# Flask route to display ITM probability table
@server.route("/itm-probability")
def display_table():
    data = generate_itm_data()
    table_html = data.to_html(index=False)
    html_content = f"""
    <html>
        <head><title>ITM Probability Table</title></head>
        <body>
            <h2 style='text-align: center;'>ITM Probability vs. Days to Expiration</h2>
            <div style='width: 80%; margin: auto;'>
                {table_html}
            </div>
        </body>
    </html>
    """
    return render_template_string(html_content)

# Dash App Layout
app.layout = html.Div([
    html.Div([
        html.H2("Market Dashboard", style={'color': 'white', 'margin': '0', 'padding': '10px'}),
        html.Nav([
            html.Ul([
                html.Li(html.A("Straddle Chart", href="#", id='menu-straddle', n_clicks=0, style={'color': 'white', 'textDecoration': 'none'})),
                html.Li(html.A("Stock Table", href="#", id='menu-stock', n_clicks=0, style={'color': 'white', 'textDecoration': 'none'})),
                html.Li(html.A("Option Chain", href="#", id='menu-option-chain', n_clicks=0, style={'color': 'white', 'textDecoration': 'none'})),
                html.Li(html.A("ITM Prob", href="/itm-probability", style={'color': 'white', 'textDecoration': 'none'}, target="_blank"))
            ], style={'listStyle': 'none', 'display': 'flex', 'gap': '20px', 'margin': '0'})
        ], style={'padding': '10px'})
    ], style={'backgroundColor': '#333', 'color': 'white', 'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'}),

    html.H2("Real-Time Market Dashboard", style={'textAlign': 'center', 'marginTop': '20px'}),

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='strike-price-dropdown',
                options=[{'label': str(strike), 'value': strike} for strike in strikes],
                value=23000,
                style={'width': '90%', 'margin': '0 auto'}
            ),
            dcc.Graph(id='live-straddle-chart', style={'height': '60vh', 'width': '100%'}),
            html.Div(id='alert-message', style={'textAlign': 'center', 'color': 'red', 'fontSize': 24})
        ], id='straddle-section', style={'display': 'block', 'padding': '10px'}),

        html.Div([
            dash_table.DataTable(
                id='live-stock-table',
                columns=[
                    {'name': 'Stock Name', 'id': 'Stock Name'},
                    {'name': 'Price', 'id': 'Price'}
                ],
                data=generate_stock_data().to_dict('records'),
                style_table={'width': '90%', 'margin': '0 auto'},
                style_cell={'textAlign': 'center', 'padding': '5px'},
                style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
                style_data_conditional=[
                    {
                        'if': {'column_id': 'Price'},
                        'backgroundColor': 'rgb(248, 248, 255)',
                        'color': 'black'
                    }
                ]
            )
        ], id='stock-section', style={'display': 'none', 'padding': '10px'}),

        html.Div([
            dash_table.DataTable(
                id='option-chain-table',
                columns=[
                    {'name': 'Call OI', 'id': 'Call OI'},
                    {'name': 'Call ChangeInOI', 'id': 'Call ChangeInOI'},
                    {'name': 'Call Price', 'id': 'Call Price'},
                    {'name': 'Strike Price', 'id': 'Strike Price'},
                    {'name': 'Put OI', 'id': 'Put OI'},
                    {'name': 'Put ChangeInOI', 'id': 'Put ChangeInOI'},
                    {'name': 'Put Price', 'id': 'Put Price'}
                ],
                data=generate_option_chain_data().to_dict('records'),
                style_table={'width': '90%', 'margin': '0 auto'},
                style_cell={'textAlign': 'center', 'padding': '5px'},
                style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
                style_data_conditional=[
                    {
                        'if': {
                            'filter_query': '{Call ChangeInOI} > 0',
                            'column_id': 'Call ChangeInOI'
                        },
                        'color': 'green'
                    },
                    {
                        'if': {
                            'filter_query': '{Call ChangeInOI} < 0',
                            'column_id': 'Call ChangeInOI'
                        },
                        'color': 'red'
                    },
                    {
                        'if': {
                            'filter_query': '{Put ChangeInOI} > 0',
                            'column_id': 'Put ChangeInOI'
                        },
                        'color': 'green'
                    },
                    {
                        'if': {
                            'filter_query': '{Put ChangeInOI} < 0',
                            'column_id': 'Put ChangeInOI'
                        },
                        'color': 'red'
                    }
                ]
            )
        ], id='option-chain-section', style={'display': 'none', 'padding': '10px'})
    ]),

    html.Div(id='india-vix-value', style={'textAlign': 'center', 'color': 'blue', 'fontSize': 24, 'marginTop': '20px'}),

    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # Update every 5 seconds
        n_intervals=0
    )
])

# Callback to update India VIX value
@app.callback(
    Output('india-vix-value', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_india_vix(n_intervals):
    return f"India VIX: {generate_india_vix()}"

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run_server(host="0.0.0.0", port=port, debug=True)
