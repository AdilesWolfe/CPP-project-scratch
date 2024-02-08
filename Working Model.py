import base64
import dash
from dash import dcc, html
from nsepython import equity_history
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import datetime

# Read the image file
with open("Assets/stock-icon.png", "rb") as f:
    image_data = f.read()

# Encode the image as a base64 string
encoded_image = base64.b64encode(image_data).decode()

start = (datetime.datetime.today() - datetime.timedelta(days=90)).strftime("%d-%m-%Y")
end = datetime.datetime.today().strftime("%d-%m-%Y")

app = dash.Dash()

app.layout = html.Div([
    html.Div([
        html.H1(children="Stock App"),
        html.Img(src=f"data:image/png;base64,{encoded_image}", style={'width': '100px'})
    ], className="banner"),
    html.Div([
        html.Label("Enter a valid Indian Stock Code"),
        html.Br(),
        dcc.Input(
            id='stock_input',
            placeholder='Ex: SBIN',
            type='text',
            value=''
        ),
        html.Button(id="submit-button",n_clicks=0, children="Submit")],className="input"),
    html.Div(
        style={'width':'1100px', 'overflow':'auto'},
        children=[dcc.Graph(id="Stock Chart", figure={})],
        className="frame"
    ),
    html.Div(
        id='alert-container',children=[
            dbc.Alert(id='alert', children='Invalid Stock Code', style={'display':'none'},is_open='')
        ])
], className="main-div")

@app.callback(
    [Output('Stock Chart', 'figure'), Output('alert','is_open')],
    [Input('submit-button', 'n_clicks')],
    [State('stock_input', 'value')]
)
def update_chart(n_clicks,stocks):
    if stocks is None or stocks=='':
        return {
            'data': [],
            'layout':{'title':'No Data Entered'}
        }, True

    try:
        equity_history(stocks,'EQ','01-01-2023','01-02-2023')
    except Exception as e:
        return( 
            {
            'data': [],
            'layout':{'title':'No Data Entered'}
        }, True )

    sym = stocks.upper()
    ser = "EQ"
    df = equity_history(stocks, ser, start, end)

    fig = go.Figure(data=[
        go.Candlestick(
            x=df['CH_TIMESTAMP'],
            open=df['CH_OPENING_PRICE'],
            high=df['CH_TRADE_HIGH_PRICE'],
            low=df['CH_TRADE_LOW_PRICE'],
            close=df['CH_CLOSING_PRICE']
        )], layout=dict(title=sym, height=500, margin=dict(l=100, r=0, t=50, b=0))
    )
    return fig, False

if __name__ == "__main__":
    app.run_server(debug=True)