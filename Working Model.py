import base64
import dash
from dash import dcc, html
from nsepython import equity_history
import plotly.graph_objects as go
from dash.exceptions import  PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from datetime import datetime as dt
from AI_model import prediction

# Read the image file
with open("Assets/stock-icon.png", "rb") as f:
    image_data = f.read()

# Encode the image as a base64 string
encoded_image = base64.b64encode(image_data).decode()

def get_stock_graph(df):
     Candlefig = go.Candlestick(
            x=df['CH_TIMESTAMP'],
            open=df['CH_OPENING_PRICE'],
            high=df['CH_TRADE_HIGH_PRICE'],
            low=df['CH_TRADE_LOW_PRICE'],
            close=df['CH_CLOSING_PRICE']
        )
     return Candlefig

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
                html.Label("✨Enter a valid Indian Stock Code✨"),
                html.Br(),
                dcc.Input(
                    id='stock_input',
                    placeholder='Ex: SBIN',
                    type='text',
                    value=''
                ),
                html.Button("Submit", id="submit-button", n_clicks=0),
                
            ],
            className="input"
        ),
        html.Div([
            dcc.DatePickerRange(id='date-picker',
                display_format=('DD/MM/YYYY'),
                min_date_allowed=dt(1995, 8, 5),
                max_date_allowed=dt.now(),
                initial_visible_month=dt.now(),
                end_date=dt.now().date())
            ], 
            className="input"
        ),
        html.Div(
            dcc.Graph(id="Stock Chart", figure={}),
            className="frame",
        ),
        html.Div(
            id='alert-container',
            children=[
                dbc.Alert(id='alert', children='⚠️Invalid Stock Code⚠️', color="warning", is_open='False', dismissable="True")
            ], className='alert-container' ),
        html.Div([
            html.Label("Enter number of days to forecast"),
            html.Br(),
            dcc.Input(id='forecast-input', 
                      type='text',
                      value='',
                      placeholder='Ex.10 '),
            html.Button('Forecast', id='forecast-btn', n_clicks=0)
            ], className="input"
        ),
        html.Div(
            dcc.Graph(id='forecast-graph', figure={}),
            className='frame'
        )
    ],
    className="main-div"
)

# callback for stock chart 
@app.callback(
    [Output('Stock Chart', 'figure'), Output('alert', 'is_open')],
    [Input('submit-button', 'n_clicks'), Input('date-picker', 'start_date'), Input('date-picker', 'end_date')],
    [State('stock_input', 'value')]
)
def update_chart(n_clicks, start_date, end_date, stocks):
    if  not n_clicks:
        return {}, False
    
    if stocks==None:
        raise PreventUpdate
        return {}, True
    else:
        try:
            start_date = dt.strptime(start_date.split('T')[0], '%Y-%m-%d').strftime('%d-%m-%Y')
            end_date = dt.strptime(end_date.split('T')[0], '%Y-%m-%d').strftime('%d-%m-%Y')
            df=equity_history(stocks, 'EQ', start_date, end_date)
            if 'CH_TIMESTAMP' not in df.columns:
                raise Exception(f"No data found for {stocks}")
        except  Exception as e:
            print(e)
            return {
            'data': [],
            'layout': {'title': 'No Data Entered'}
            }, True

    ser = "EQ"
    df = equity_history(stocks, ser, start_date, end_date)
    fig={'data':[get_stock_graph(df)],
         'layout':dict(title=("📊"+stocks+"📊"), height=500, margin=dict(l=100, r=0, t=50, b=0))}
   
    return fig, False

# Callback to generate forecast and display
@app.callback(
    [Output('forecast-graph', 'figure')],
    [Input('forecast-btn', 'n_clicks')],
    [State('forecast-input','value'), State('stock_input', 'value')]
)
def generate_forecast(n_clicks,days,stocks):
    if not n_clicks or days is None or stocks is None :
        return {}
    else:
        fig=(prediction(stocks, days))
    return [fig]
if __name__ == "__main__":
    app.run_server(debug=True)