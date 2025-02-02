import dash
from dash import dcc, html, dash_table
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go
import pandas as pd
import random
import datetime

# Initialize the Dash app
app = dash.Dash(__name__)

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

# App layout
app.layout = html.Div([
    html.Div([
        html.H2("Market Dashboard", style={'color': 'white', 'margin': '0', 'padding': '10px'}),
        html.Nav([
            html.Ul([
                html.Li(html.A("Straddle Chart", href="#", id='menu-straddle', n_clicks=0, style={'color': 'white', 'textDecoration': 'none'})),
                html.Li(html.A("Stock Table", href="#", id='menu-stock', n_clicks=0, style={'color': 'white', 'textDecoration': 'none'})),
                html.Li(html.A("Option Chain", href="#", id='menu-option-chain', n_clicks=0, style={'color': 'white', 'textDecoration': 'none'})),
                html.Li(html.A("ITM Prob", href="#", id='menu-option-chain', n_clicks=0, style={'color': 'white', 'textDecoration': 'none'}))
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

# Callback to toggle between sections
@app.callback(
    [Output('straddle-section', 'style'),
     Output('stock-section', 'style'),
     Output('option-chain-section', 'style')],
    [Input('menu-straddle', 'n_clicks'),
     Input('menu-stock', 'n_clicks'),
     Input('menu-option-chain', 'n_clicks')],
    [State('straddle-section', 'style'),
     State('stock-section', 'style'),
     State('option-chain-section', 'style')]
)
def toggle_sections(n_straddle, n_stock, n_option_chain, straddle_style, stock_style, option_chain_style):
    ctx = dash.callback_context
    if not ctx.triggered:
        return straddle_style, stock_style, option_chain_style
    else:
        clicked_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if clicked_id == 'menu-straddle':
            return {'display': 'block', 'padding': '10px'}, {'display': 'none', 'padding': '10px'}, {'display': 'none', 'padding': '10px'}
        elif clicked_id == 'menu-stock':
            return {'display': 'none', 'padding': '10px'}, {'display': 'block', 'padding': '10px'}, {'display': 'none', 'padding': '10px'}
        elif clicked_id == 'menu-option-chain':
            return {'display': 'none', 'padding': '10px'}, {'display': 'none', 'padding': '10px'}, {'display': 'block', 'padding': '10px'}
    return straddle_style, stock_style, option_chain_style

# Function to simulate price updates and store straddle prices
def update_prices_and_straddle(strike):
    call_price = prices[strike]['call'] + random.uniform(-2, 2)
    put_price = prices[strike]['put'] + random.uniform(-2, 2)
    call_price = max(call_price, 0)
    put_price = max(put_price, 0)

    straddle_price = call_price + put_price
    prices[strike]['call'] = call_price
    prices[strike]['put'] = put_price
    prices[strike]['straddle'].append(straddle_price)

    if len(prices[strike]['straddle']) > 60:
        prices[strike]['straddle'] = prices[strike]['straddle'][-60:]

    return straddle_price

# Callback to update the graph and check for alerts
@app.callback(
    [Output('live-straddle-chart', 'figure'),
     Output('alert-message', 'children'),
     Output('live-stock-table', 'data'),
     Output('option-chain-table', 'data')],
    [Input('interval-component', 'n_intervals'),
     Input('strike-price-dropdown', 'value')]
)
def update_dashboard(n, selected_strike):
    global time_series

    # Update prices and straddle for selected strike
    straddle_price = update_prices_and_straddle(selected_strike)

    # Update time series
    time_series.append(datetime.datetime.now())
    if len(time_series) > 60:
        time_series = time_series[-60:]

    # Generate alert message
    alert_message = ""
    if straddle_price >= 500:
        alert_message = f"Alert: Straddle price for {selected_strike} has reached or exceeded 500!"
    elif straddle_price <= 300:
        alert_message = f"Alert: Straddle price for {selected_strike} has dropped to or below 300!"

    # Prepare line chart data for plotting
    straddle_data = prices[selected_strike]['straddle']
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_series[-len(straddle_data):],
        y=straddle_data,
        mode='lines+markers',
        name=f'Straddle Price {selected_strike}'
    ))
    fig.update_layout(title=f'Live Straddle Price ({selected_strike} Strike)', xaxis_title='Time', yaxis_title='Price', showlegend=True)

    # Update stock table data
    stock_data = generate_stock_data()

    # Update option chain data
    option_chain_data = generate_option_chain_data()

    return fig, alert_message, stock_data.to_dict('records'), option_chain_data.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
