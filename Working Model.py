import base64
from datetime import datetime as dt
import dash
from dash import dcc, html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from nsepython import equity_history
from AI_model import prediction
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Read the image file
with open("Assets/stock-icon.png", "rb") as f:
    image_data = f.read()

# Encode the image as a base64 string
encoded_image = base64.b64encode(image_data).decode()

def get_stock_graph(df):
    Candlefig = go.Figure(data=[
        go.Candlestick(
            x=df['CH_TIMESTAMP'],
            open=df['CH_OPENING_PRICE'],
            high=df['CH_TRADE_HIGH_PRICE'],
            low=df['CH_TRADE_LOW_PRICE'],
            close=df['CH_CLOSING_PRICE']
        )]
    )
    Candlefig.update_layout(title_text="Stock Chart", height=500, margin=dict(l=100, r=0, t=50, b=0))
    return Candlefig

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("InvestIQ"),
                html.Img(src=f"data:image/png;base64,{encoded_image}", style={'width': '100px'})
            ],
            className="banner",
        ),
       html.Div(
    [
        html.Label("✨Enter a valid Indian Stock Code✨", className="input-label", style={'margin': '10px'}),
        dcc.Input(
            id='stock_input',
            placeholder='Ex: SBIN',
            type='text',
            value='',
            className="input-fieldd",
            style={'margin': '20px'}
        ),
        html.Label("✨Select appropriate time line✨", className="input-labell", style={'margin': '10px'}),
        dcc.DatePickerRange(
            id='date-picker',
            display_format='DD/MM/YYYY',
            min_date_allowed=dt(1995, 8, 5),
            max_date_allowed=dt.now(),
            initial_visible_month=dt.now(),
            end_date=dt.now().date(),
            className="input-field",
            style={'margin': '20px'}
        ),
        html.Button("Submit", id="submit-button", n_clicks=0, className="submit-button",
                    style={'border': '3px solid black '})
    ],
    className="input-container", 
    style={'border': '3px solid white ', 'padding': '10px', 'background-color': 'black', 'border-radius': '10px'}
),
 html.Br(),
  html.Br(),
  html.Br(),
 
        html.Div(id="alert-container", className="alert-container"),
        html.Div(
            [
                html.Div(id="stock-chart-container"),
                html.Div(id="forecast-graph-container",style={'margin-top': '20px'})  # Apply margin-top here
            ]
        )
    ], className='main-div'
)


@app.callback(
    Output('stock-chart-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('stock_input', 'value'),
     State('date-picker', 'start_date'),
     State('date-picker', 'end_date')]
)
def update_stock_chart(n_clicks, stock_input, start_date, end_date):
    if not n_clicks:
        raise PreventUpdate

    if not stock_input:
        return {}

    try:
        start_date = dt.strptime(start_date.split('T')[0], '%Y-%m-%d').strftime('%d-%m-%Y')
        end_date = dt.strptime(end_date.split('T')[0], '%Y-%m-%d').strftime('%d-%m-%Y')
        
        df = equity_history(stock_input, 'EQ', start_date, end_date)
        
        if df.empty:
            raise Exception("No data found for the given stock code and date range.")

        fig = get_stock_graph(df)
        return dcc.Graph(id="Stock Chart", figure=fig)

    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger", dismissable=True)

@app.callback(
    Output('forecast-graph-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('stock_input', 'value'),
     State('date-picker', 'start_date'),
     State('date-picker', 'end_date')]
)
def generate_forecast(n_clicks, stock_input, start_date, end_date):
    if not n_clicks or not stock_input:
        raise PreventUpdate

    try:
        # Check if the data is valid before generating the forecast graph
        start_date = dt.strptime(start_date.split('T')[0], '%Y-%m-%d').strftime('%d-%m-%Y')
        end_date = dt.strptime(end_date.split('T')[0], '%Y-%m-%d').strftime('%d-%m-%Y')
        
        df = equity_history(stock_input, 'EQ', start_date, end_date)
        
        if df.empty:
            raise Exception("No data found for the given stock code and date range.")

        # Dummy implementation of forecast graph
        fig = go.Figure(data=go.Scatter(x=[1, 2, 3], y=[4, 1, 2]))
        fig.update_layout(title_text="Forecast Graph", height=500, margin=dict(l=100, r=0, t=50, b=0))
        return dcc.Graph(id="Forecast Graph", figure=fig)

    except Exception as e:
        # Hide the forecast graph and display an alert
        return [dbc.Alert(f"Error: {str('Enter Valid Data...')}", color="danger", dismissable=True), html.Div()]
        # Returning an empty div to hide the forecast graph

if __name__ == "__main__":
    app.run_server(debug=True)
