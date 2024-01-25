import datetime
from nsepython import equity_history
import plotly.graph_objects as go

end_date= datetime.datetime.now().strftime("%d-%m-%Y")
end_date= str(end_date)

start_date= (datetime.datetime.now()-datetime.timedelta(days=65)).strftime("%d-%m-%Y")
start_date=str(start_date)

symbol="SBIN"
series="EQ"
df= equity_history(symbol,series,start_date,end_date)

fig = go.Figure(data=[go.Candlestick(x=df['CH_TIMESTAMP'],
                open=df['CH_OPENING_PRICE'],
                high=df['CH_TRADE_HIGH_PRICE'],
                low=df['CH_TRADE_LOW_PRICE'],
                close=df['CH_CLOSING_PRICE'])])
fig.show()