import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc

# Initialize the Dash app with Bootstrap for easy styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sidebar styling
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '250px',
    'padding': '20px',
    'background-color': '#111',
    'color': 'white',
    'transition': '0.3s',
}

SIDEBAR_HIDDEN = SIDEBAR_STYLE.copy()
SIDEBAR_HIDDEN['margin-left'] = '-250px'

# Content styling
CONTENT_STYLE = {
    'margin-left': '250px',
    'padding': '20px',
    'transition': '0.3s',
}

CONTENT_EXPANDED_STYLE = CONTENT_STYLE.copy()
CONTENT_EXPANDED_STYLE['margin-left'] = '0'

# Layout
app.layout = html.Div([
    # Sidebar toggle button
    html.Button('☰', id='toggle-button', style={
        'position': 'fixed',
        'top': '20px',
        'left': '20px',
        'zIndex': 1,
        'fontSize': '24px',
        'background-color': '#111',
        'color': 'white',
        'border': 'none',
        'padding': '10px 15px',
        'cursor': 'pointer'
    }),
    
    # Sidebar navigation
    html.Div(id='sidebar', children=[
        html.H2('Sidebar Menu', className='display-4'),
        html.Hr(),
        html.P('Navigation Links', className='lead'),
        dbc.Nav([
            dbc.NavLink('Home', href='#', id='home-link', active='exact'),
            dbc.NavLink('About', href='#', id='about-link', active='exact'),
            dbc.NavLink('Contact', href='#', id='contact-link', active='exact'),
        ], vertical=True, pills=True),
    ], style=SIDEBAR_STYLE),
    
    # Main content area
    html.Div(id='page-content', style=CONTENT_STYLE)
])

# Callback to toggle sidebar
@app.callback(
    [Output('sidebar', 'style'), Output('page-content', 'style')],
    [Input('toggle-button', 'n_clicks')]
)
def toggle_sidebar(n):
    if n and n % 2 == 1:
        return SIDEBAR_HIDDEN, CONTENT_EXPANDED_STYLE
    else:
        return SIDEBAR_STYLE, CONTENT_STYLE

# Callback to update content based on sidebar navigation
@app.callback(
    Output('page-content', 'children'),
    [Input('home-link', 'n_clicks'),
     Input('about-link', 'n_clicks'),
     Input('contact-link', 'n_clicks')]
)
def display_page(home_clicks, about_clicks, contact_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return html.H1('Welcome!', style={'textAlign': 'center'})
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'about-link':
            return html.Div([
                html.H1('About Page', style={'textAlign': 'center'}),
                html.Iframe(
                    src='https://www.moneycontrol.com/earnings-calendar',
                    style={'width': '100%', 'height': '80vh', 'border': 'none'}
                )
            ])
        elif button_id == 'contact-link':
            return html.Div([
                html.H1('Contact Page', style={'textAlign': 'center'}),
                html.P('Email us at contact@example.com', style={'textAlign': 'center'})
            ])
        else:
            return html.Div([
                html.H1('Home Page', style={'textAlign': 'center'}),
                html.P('Welcome to the Home Page!', style={'textAlign': 'center'})
            ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
