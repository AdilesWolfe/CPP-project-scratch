import dash
from dash import dcc
from dash import html
from nsepython import equity_history
import plotly.graph_objects as go
import datetime

start= str((datetime.datetime.today()-datetime.timedelta(days=365)).strftime("%d-%m-%Y"))
end=str(datetime.datetime.today().strftime("%d-%m-%Y"))

sym="NHPC"
ser="EQ"
df=equity_history(sym,ser,start,end)
#print(df.head())

fig=go.Figure(data=[go.Candlestick(x=df['CH_TIMESTAMP'],
                    open=df['CH_OPENING_PRICE'],
                    high=df['CH_TRADE_HIGH_PRICE'],
                    low=df['CH_TRADE_LOW_PRICE'],
                        close=df['CH_CLOSING_PRICE'])],
              layout=dict(title=sym))                   


app= dash.Dash()

app.layout= html.Div([
    html.Div(html.H1(children="Hello World")),
    html.Label("DASH GRAPH"),
    html.Div(
        dcc.Input(
            id='stock_input',
            placeholder='Enter a valid Indian Stock Code',
            type='text',
            value=''
        )
    ),
    html.Div(
        dcc.Graph(id="Stock Chart",
                  figure=fig),
    )
])

if __name__== "__main__":
    app.run_server(debug=True)