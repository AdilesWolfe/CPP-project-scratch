from turtle import position, width
import dash
from dash import dcc
from dash import html
from nsepython import equity_history
import plotly.graph_objects as go
import datetime

app= dash.Dash()

app.layout= html.Div([
    html.Div([html.H1(children="Stock App"),
             html.Img(src="Assets/stock-icon.png")],className="banner"),
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
        style={'width':'1100px', 'overflow':'auto'},
        children=[dcc.Graph(id="Stock Chart",
                  figure={})]
    )
])

@app.callback(
    dash.dependencies.Output('Stock Chart', 'figure'),
    [dash.dependencies.Input('stock_input', 'value')]
)

def update_chart(stocks):
    if  stocks is None:
        return {}
    start= str((datetime.datetime.today()-datetime.timedelta(days=90)).strftime("%d-%m-%Y"))
    end=str(datetime.datetime.today().strftime("%d-%m-%Y"))
    sym=stocks
    ser="EQ"
    df=equity_history(sym,ser,start,end)

    fig=go.Figure(data=[
        go.Candlestick(
            x=df['CH_TIMESTAMP'],
            open=df['CH_OPENING_PRICE'],
            high=df['CH_TRADE_HIGH_PRICE'],
            low=df['CH_TRADE_LOW_PRICE'],
            close=df['CH_CLOSING_PRICE']
        )],layout=dict(title=sym, height=500, margin=dict(l=0, r=0,t=0,b=0))
        
    )
    return fig

if __name__== "__main__":
    app.run_server(debug=True)