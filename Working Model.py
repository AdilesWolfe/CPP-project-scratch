import base64
import dash
from dash import dcc, html
from nsepython import equity_history
import plotly.graph_objects as go
import datetime

# Read the image file
with open("stockicon.png", "rb") as f:
    image_data = f.read()

# Encode the image as a base64 string
encoded_image = base64.b64encode(image_data).decode()

app = dash.Dash(__name__)

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
            value='SBIN'
        )
    ]),
    html.Div(
        style={'width': '1100px', 'overflow': 'auto', 'align': 'center'},
        children=[dcc.Graph(id="Stock Chart", figure={})],
        className="frame"
    )
], className="main-div")

@app.callback(
    dash.dependencies.Output('Stock Chart', 'figure'),
    [dash.dependencies.Input('stock_input', 'value')]
)
def update_chart(stocks):
    if stocks is None:
        return {}
    start = (datetime.datetime.today() - datetime.timedelta(days=90)).strftime("%d-%m-%Y")
    end = datetime.datetime.today().strftime("%d-%m-%Y")
    sym = stocks
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
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
