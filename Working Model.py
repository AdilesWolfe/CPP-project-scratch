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

app = dash.Dash()

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(children="Stock App"),
                html.Img(
                    src=f"data:image/png;base64,{encoded_image}", style={'width': '100px'})
            ],
            className="banner",
        ),
        html.Div(
            [
                html.Label("Enter a valid Indian Stock Code"),
                html.Br(),
                dcc.Input(
                    id='stock_input',
                    placeholder='Ex: SBIN',
                    type='text',
                    value=''
                ),
                html.Button(id="submit-button", n_clicks=0, children="Submit"),
                html.Label("Select a start date"),
                dcc.DatePickerSingle(
                    id='start-date',
                    display_format='DD/MM/YY',
                    min_date_allowed=datetime.datetime(2022, 1, 1),
                    max_date_allowed=datetime.datetime.today(),
                    initial_visible_month=datetime.datetime(2022, 1, 1),
                    date=datetime.datetime(2022, 1, 1)
                ),
                html.Label("Select an end date"),
                dcc.DatePickerSingle(
                    id='end-date',
                    display_format='DD/MM/YY',
                    min_date_allowed=datetime.datetime(2022, 1, 1),
                    max_date_allowed=datetime.datetime.today(),
                    initial_visible_month=datetime.datetime.today(),
                    date=datetime.datetime.today()
                ),
            ],
            className="input",
        ),
        html.Div(
            dcc.Graph(id="Stock Chart", figure={}),
            className="frame",
        ),
        html.Div(
            id='alert-container',
            children=[
                dbc.Alert(id='alert', children='Invalid Stock Code', color="warning", is_open='False', dismissable="True")
            ])
    ],
    className="main-div"
)

@app.callback(
    [Output('Stock Chart', 'figure'), Output('alert', 'is_open')],
    [Input('submit-button', 'n_clicks'), Input('start-date', 'date'), Input('end-date', 'date')],
    [State('stock_input', 'value')]
)
def update_chart(n_clicks, start_date, end_date, stocks):
    if not start_date or not end_date or stocks is None or stocks == '':
        return {
            'data': [],
            'layout': {'title': 'No Data Entered'}
        }, True

    try:
        start_date = datetime.datetime.strptime(start_date.split('T')[0], '%Y-%m-%d').strftime('%d-%m-%Y')
        end_date = datetime.datetime.strptime(end_date.split('T')[0], '%Y-%m-%d').strftime('%d-%m-%Y')
        equity_history(stocks, 'EQ', start_date, end_date)
    except Exception as e:
        print(f"Error: {e}")
        return {
            'data': [],
            'layout': {'title': 'No Data Entered'}
        }, True

    sym = stocks.upper()
    ser = "EQ"
    df = equity_history(stocks, ser, start_date, end_date)

    Candlefig = go.Figure(data=[
        go.Candlestick(
            x=df['CH_TIMESTAMP'],
            open=df['CH_OPENING_PRICE'],
            high=df['CH_TRADE_HIGH_PRICE'],
            low=df['CH_TRADE_LOW_PRICE'],
            close=df['CH_CLOSING_PRICE']
        )],
        layout=dict(title=sym, height=500, margin=dict(l=100, r=0, t=50, b=0))
    )
    return Candlefig, False

if __name__ == "__main__":
    app.run_server(debug=True)
