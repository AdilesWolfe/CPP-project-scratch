import base64
from datetime import datetime as dt
import dash
from dash import dcc, html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from nsepython import equity_history
import dash_bootstrap_components as dbc

from AI_model import prediction

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Read the image files and encode them as base64 strings
with open("Assets/line.gif", "rb") as f:
    image_data = f.read()

with open("Assets/cover.png", "rb") as l:
    image_dat = l.read()

with open("Assets/newwww.png", "rb") as n:
    image_da = n.read()

with open("Assets/namee.png", "rb") as t:
    image_d = t.read()

encoded_image = base64.b64encode(image_data).decode()
encoded_imagee = base64.b64encode(image_dat).decode()
encoded_imageee = base64.b64encode(image_da).decode()
encoded_imageeee = base64.b64encode(image_d).decode()

# Function to generate the stock chart
def get_stock_graph(df, stock_name):
    Candlefig = go.Figure(data=[
        go.Candlestick(
            x=df['CH_TIMESTAMP'],
            open=df['CH_OPENING_PRICE'],
            high=df['CH_TRADE_HIGH_PRICE'],
            low=df['CH_TRADE_LOW_PRICE'],
            close=df['CH_CLOSING_PRICE']
        )]
    )
    Candlefig.update_layout(title_text=f"Stock Chart for {stock_name}", height=500, margin=dict(l=100, r=0, t=50, b=0))
    return Candlefig

# Define the layout of the app
app.layout = html.Div(
    [
        html.Div(
            [
                html.H1([
                    html.Img(src=f"data:image/png;base64,{encoded_imageeee}", style={'width': '180px', 'margin-right': '10px', 'border-radius':'45px'})
                ], style={'animation': 'fadeIn 3s linear'}),  # Animation effect added here
                html.Img(src=f"data:image/png;base64,{encoded_image}", style={'width': '100px', 'border-radius': '30px', 'border': '3px solid black'})
            ],
            className="banner",
        ),
        html.Div(
            [
                html.Label("Enter a valid Indian Stock Code", className="input-label"),
                dcc.Input(
                    id='stock_input',
                    placeholder='Ex: SBIN',
                    type='text',
                    value='',
                    className="input-fieldd",
                    style={'margin': '20px', 'border': '3px solid black'}
                ),
                html.Label("Select appropriate timeline", className="input-labell"),
                dcc.DatePickerRange(
                    id='date-picker',
                    display_format='DD/MM/YYYY',
                    min_date_allowed=dt(1995, 8, 5),
                    max_date_allowed=dt.now(),
                    initial_visible_month=dt.now(),
                    end_date=dt.now().date(),
                    className="input-field",
                    style={'margin': '20px', 'border': '3px solid black'}
                ),
                html.Button("Submit", id="submit-button", n_clicks=0, className="submit-button", style={'border': '3px solid black'})
            ],
            className="input-container",
            style={'border': '3px solid Black', 'padding': '60px','background-image': f'url(data:image/png;base64,{encoded_imagee})'}
        ),
        html.Hr(style={'padding': '5px'}, className='hhr'),
        html.Div(
            [
                html.Div(
                    [
                        html.P("Stocks visualization and forecasting involve the graphical representation of historical stock price data and the prediction of future price movements. Visualization techniques include candlestick charts, line graphs, and scatter plots, which provide insights into past trends and patterns in stock prices. Forecasting, on the other hand, utilizes statistical models, machine learning algorithms, and artificial intelligence to analyze historical data and predict future stock prices. These forecasts assist investors, traders, and analysts in making informed decisions about buying, selling, or holding stocks by providing insights into potential future market trends and price movements.", className='para1'),
                        html.P("Stock price prediction (SPP) is the process of forecasting future movements in the value of a particular stock or a basket of stocks. It involves analyzing historical price data, market trends, trading volumes, and various other factors to develop predictive models that can estimate the future price of a stock. SPP is essential for investors, traders, and financial analysts to make informed decisions about buying, selling, or holding stocks. Techniques such as machine learning, artificial intelligence, and statistical modeling are commonly employed in SPP to analyze large datasets and identify patterns that may indicate future price movements. Despite its challenges and inherent uncertainty, SPP plays a crucial role in financial markets by providing insights into potential investment opportunities and risks. ", className='para2'),
                    ],
                    className="para-container"
                ),
                html.Div(id="alert-container", className="alert-container"),
                html.Div(
                    [
                        dcc.Loading(
                            id="loading-output",
                            children=[
                                html.Div(id="stock-chart-container", style={'margin-bottom': '40px'}),
                                html.Div(id="forecast-graph-container", style={'margin-top': '40px'})  # Apply margin-top here
                            ],
                            type="circle", color='white'
                        )
                    ], className='loading-outputt'
                )
            ], className='main-div',
            style={'background-image': f'url(data:image/png;base64,{encoded_imageee})'}
        )
    ]
)

# Callback to update the stock chart based on user input
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

        fig = get_stock_graph(df, stock_input)  # Pass stock name to the function
        return dcc.Graph(id="Stock Chart", figure=fig, className='frame')

    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger", dismissable=True)


# Callback to generate the forecast graph based on user input
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
        fig = prediction(stock_input, 7)
        fig.update_layout(title_text="Forecast Graph", height=500, margin=dict(l=100, r=0, t=50, b=0))
        return [dcc.Graph(id='forecast-graph', figure=fig, className='forecast-graph')]

    except Exception as e:
        # Hide the forecast graph and display an alert
        return [dbc.Alert(f"Error: {str('Enter Valid Data...')}", color="danger", dismissable=True), html.Div()]

if __name__ == "__main__":
    app.run_server(debug=True)