from datetime import datetime as dt
import base64
import dash
from dash import dcc, html
from nsepython import equity_history
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from AI_model import prediction

# Initialize Dash app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Read the image files and encode them as base64 strings
with open("Assets/line.gif", "rb") as f:
    image_data = f.read()

with open("Assets/cover.png", "rb") as l:
    image_dat = l.read()

with open("Assets/newwww.png", "rb") as n:
    image_da = n.read()

with open("Assets/namee.png", "rb") as t:
    image_d = t.read()

with open('Assets/pran.png', "rb") as s:
    ima_d = s.read()

with open('Assets/desig.png', "rb") as o:
    ima = o.read()

with open('Assets/aadit.png', "rb") as w:
    im = w.read()

with open('Assets/shah.jpg', "rb") as y:
    i = y.read()

with open('Assets/cmd.png', "rb") as b:
    l = b.read()

with open('Assets/port.jpg', "rb") as h:
    q = h.read()

with open('Assets/edu.jpg', "rb") as z:
    x = z.read()

with open('Assets/risk.jpg', "rb") as zz:
    xx = zz.read()

with open('Assets/eng.jpg', "rb") as zzz:
    ll = zzz.read()

encoded_image = base64.b64encode(image_data).decode()
encoded_imagee = base64.b64encode(image_dat).decode()
encoded_imageee = base64.b64encode(image_da).decode()
encoded_imageeee = base64.b64encode(image_d).decode()
encoded_image1 = base64.b64encode(ima_d).decode()
encoded_image11 = base64.b64encode(ima).decode()
encoded_image111 = base64.b64encode(im).decode()
encoded_image12 = base64.b64encode(i).decode()
encoded_image22 = base64.b64encode(l).decode()
encoded_image222 = base64.b64encode(q).decode()
encoded_imagee222 = base64.b64encode(x).decode()
encoded_imagee22 = base64.b64encode(xx).decode()
e = base64.b64encode(ll).decode()

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


# Define the layout of the navigation menu
nav_menu = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("AI Predictor", href="/AI-Predictor")),
        dbc.NavItem(dbc.NavLink("Top 50 Indian Stocks", href="/top-50-stocks")),
        dbc.NavItem(dbc.NavLink("Why InvestIQ?", href="/why-investiq")),
        dbc.NavItem(dbc.NavLink("About Us", href="/about")),
    ],
    className="ml-auto",  # Align the menu to the right
    navbar=True,
)

# Add the header to the layout
header = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                   html.Img(src=f"data:image/png;base64,{encoded_imageeee}", style={'width': '180px', 'margin-right': '10px', 'border-radius':'45px'})
                ],
                align="center",
            ),
            href="/",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(nav_menu, id="navbar-collapse", navbar=True),
        html.A(
            html.Img(src=f"data:image/png;base64,{encoded_image}",style={'height':'45px','width': '80px', 'margin-right': '10px', 'border-radius':'25px'}),
            href="/",
            style={"position": "absolute", "right": "10px"},
        ),
    ],
    color="dark",
    dark=True,
    className="mb-5",  # Add margin at the bottom
)

# Define the layout of the top 50 Indian stocks list
top_50_stock_list = html.Div(id='stock-list-container', className='stock-list')

# Add the header to the layout
app.layout = html.Div(
    [
        header,
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', className='page-content'),
        top_50_stock_list
    ]
)

# Callback to update the top 50 Indian stocks list based on the selected link
@app.callback(
    Output('stock-list-container', 'children'),
    [Input('url', 'pathname')]
)
def update_stock_list(pathname):
    if pathname == "/top-50-stocks":  # Check if the active link is "Top 50 Indian Stocks"
        # Replace this list with your actual list of 50 stock names
        stock_names = [
    ('ASIANPAINT', ' - Asian Paints Ltd'), ('BRITANNIA', ' - Britannia Industries Ltd'), ('CIPLA', ' - Cipla Ltd'),
    ('EICHERMOT', ' - Eicher Motors Ltd'), ('NESTLEIND', ' - Nestle India Ltd'), ('GRASIM', ' - Grasim Industries Ltd'),
    ('HEROMOTOCO', ' - Hero MotoCorp Ltd'), ('HINDALCO', ' - Hindalco Industries Ltd'), ('HINDUNILVR', ' - Hindustan Unilever Ltd'),
    ('ITC', ' - ITC Ltd'), ('LT', ' - Larsen & Toubro Ltd'), ('M&M', ' - Mahindra & Mahindra Ltd'), ('RELIANCE', ' - Reliance Industries Ltd'),
    ('TATACONSUM', ' - Tata Consumer Products Ltd'), ('TATAMOTORS', ' - Tata Motors Ltd'), ('TATASTEEL', ' - Tata Steel Ltd'),
    ('WIPRO', ' - Wipro Ltd'), ('APOLLOHOSP', ' - Apollo Hospitals Enterprise Ltd'), ('DRREDDY', ' - Dr Reddys Laboratories Ltd'),
    ('TITAN', ' - Titan Company Ltd'), ('SBIN', ' - State Bank of India'), ('SRF', ' - Shriram Finance Ltd'), ('BPCL', ' - Bharat Petroleum Corporation Ltd'),
    ('KOTAKBANK', ' - Kotak Mahindra Bank Ltd'), ('INFY', ' - Infosys Ltd'), ('BAJFINANCE', ' - Bajaj Finance Ltd'),
    ('ADANIENT', ' - Adani Enterprises Ltd'), ('SUNPHARMA', ' - Sun Pharmaceuticals Industries Ltd'), ('JSWSTEEL', ' - JSW Steel Ltd'),
    ('HDFCBANK', ' - HDFC Bank Ltd'), ('TCS', ' - Tata Consultancy Services Ltd'), ('ICICIBANK', ' - ICICI Bank Ltd'),
    ('POWERGRID', ' - Power Grid Corporation of India Ltd'), ('MARUTI', ' - Maruti Suzuki India Ltd'), ('INDUSINDBK', ' - IndusInd Bank Ltd'),
    ('AXISBANK', ' - Axis Bank Ltd'), ('HCLTECH', ' - HCL Technologies Ltd'), ('ONGC', ' - Oil & Natural Gas Corpn Ltd'),
    ('NTPC', ' - NTPC Ltd'), ('COALINDIA', ' - Coal India Ltd'), ('BHARTIARTL', '-Bharti Airtel Ltd'), ('TECHM', ' - Tech Mahindra Ltd'),
    ('MINDTREE', ' - LTIMindtree Ltd'), ('DIVISLAB', ' - Divis Laboratories Ltd'), ('ADANIPORTS', ' - Adani Ports & Special Economic Zone Ltd'),
    ('HDFCLIFE', ' - HDFC Life Insurance Company Ltd'), ('SBILIFE', ' - SBI Life Insurance Company Ltd'), ('ULTRACEMCO', ' - UltraTech Cement Ltd'),
    ('BAJAJ-AUTO', ' - Bajaj Auto Ltd'), ('BAJAJFINSV', '-Bajaj Finserv Ltd')]
        # Create a list of HTML list items for each stock name
        stock_list_items = [html.Li([
                html.Span(html.B(stock_name[0]), style={'font-weight': 'bold'}),
                html.Span(stock_name[1], style={'font-weight': 'normal'})
                ]) for stock_name in stock_names]
        # Return the list of stock names
        return html.Ul(stock_list_items, className='stock-list-items')
    else:
        return None

github_icon_url = "https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png"
email_icon_url = "https://upload.wikimedia.org/wikipedia/commons/7/7e/Gmail_icon_%282020%29.svg"


# Callback to update page content based on URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/about':
        with open("Assets/aboutus.html", "r") as file:
            aboutus_content = file.read()
        return html.Div([
            html.H1("About Us", className='about-container'),
            html.H5("At InvestIQ, we're more than just a Project - we're a passionate team driven by innovation and dedicated to exceeding expectations. With a commitment to integrity, excellence, and client satisfaction, we strive to make a difference in everything we do. Our diverse expertise, collaborative approach, and unwavering focus on delivering value set us apart. Together, we're on a mission to empower our clients, inspire our communities, and shape a brighter future. Welcome to the journey with us.",className='about-container'),
            html.Div(aboutus_content),
            html.H2("Our Team", className='about-container'),
            html.H5("Teamwork is the cornerstone of success, a symphony of collaboration where individuals harmonize their unique talents toward a common goal. In the orchestra of achievement, the conductor, or team leader, is the guiding force, orchestrating unity, direction, and momentum. A great team leader inspires not only through their vision but also through their empathy, understanding each member's strengths and weaknesses to compose a cohesive ensemble. They foster an environment of trust, communication, and mutual respect, empowering each member to contribute their best while ensuring harmony amidst diversity. With a skilled leader at the helm, teams transcend boundaries, navigate challenges, and achieve greatness, transforming a mere collection of individuals into a powerhouse of collective brilliance. ________________________________________________________________________________",className='about-container'),
            html.Div([
                html.Div([
                     html.Img(src=f"data:image/png;base64,{encoded_image12}", style={'width': '100px', 'height': '100px', 'border-radius': '50%', 'margin-bottom': '10px'}),
                     html.P("Pranav Amge", style={'font-weight': 'bold'}),
                     html.H6("(Front-end Dev.)"),
                     html.A(html.Img(src=email_icon_url, style={'width': '30px', 'height': '30px', 'margin-right': '5px',}), href="mailto:amgepranav@gmail.com"),
                     html.A(html.Img(src=github_icon_url , style={'width': '30px', 'height': '30px'}), href="https://github.com/pp123344")
                ], className="member-box"),
                html.Div([
                    html.Img(src=f"data:image/png;base64,{encoded_image111}", style={'width': '100px', 'height': '100px', 'border-radius': '50%', 'margin-bottom': '10px'}),
                    html.P("Aditya Sonawane", style={'font-weight': 'bold'}),
                    html.H6("(Back-end Dev.)"),
                    html.A(html.Img(src=email_icon_url, style={'width': '30px', 'height': '30px', 'margin-right': '5px'}), href="mailto:2003adityasonawane@gmail.com"),
                    html.A(html.Img(src=github_icon_url, style={'width': '30px', 'height': '30px'}), href="https://github.com/AdilesWolfe")
                ], className="member-box"),
                html.Div([
                    html.Img(src=f"data:image/png;base64,{encoded_image1}", style={'width': '100px', 'height': '100px', 'border-radius': '50%', 'margin-bottom': '10px'}),
                    html.P("Shahid Shaikh", style={'font-weight': 'bold'}),
                    html.H6("(Front-end Dev.)"),
                    html.A(html.Img(src=email_icon_url, style={'width': '30px', 'height': '30px', 'margin-right': '5px'}), href="mailto:shahiduddin153@gmail.com"),
                    html.A(html.Img(src=github_icon_url, style={'width': '30px', 'height': '30px'}), href="https://github.com/Shahiduddin1710")
                ], className="member-box"),
                html.Div([
                    html.Img(src=f"data:image/png;base64,{encoded_image11}", style={'width': '100px', 'height': '100px', 'border-radius': '50%', 'margin-bottom': '10px'}),
                    html.P("Ayan Khan", style={'font-weight': 'bold'}),
                    html.H6("(UI Designer)"),
                    html.A(html.Img(src=email_icon_url, style={'width': '30px', 'height': '30px', 'margin-right': '5px'}), href="mailto:khanayanayub7000@gmail.com"),
                    html.A(html.Img(src=github_icon_url, style={'width': '30px', 'height': '30px'}), href="https://github.com/Ayan81690")
                ], className="member-box")
            ],className='about-container',style={'display': 'flex', 'justify-content': 'space-around', 'margin-top': '20px'})
        ],className='about-container')
    elif pathname == '/top-50-stocks':
        return html.Div([
            html.H1("Top 50 Indian Stocks", className='top-stocks-header'),
            html.P("(Stock Code - Stock Name) ____ Hint:You Can Use Ctrl+f to seach in the Top 50 Stock List.", className='top-stocks-description', style={'color':'yellow'}),
            html.Div([
                
                # Add the remaining stock names here
            ], className='top-stocks-list')
        ], className='top-stocks-container')
    elif pathname == '/why-investiq':
        return html.Div([
    html.H1("Why InvestIQ?", className='why-investiq-header'),
    html.P("InvestIQ is a cutting-edge investment platform designed to empower investors with powerful tools and insights to make informed investment decisions. Here are some reasons why you should choose InvestIQ:"),
    html.Ul([
        html.Li("Comprehensive Market Analysis: InvestIQ provides comprehensive market analysis tools, including real-time data, advanced charting, and customizable indicators, to help you analyze market trends and make informed decisions."),
        html.Li("Portfolio Management: With InvestIQ, you can easily manage your investment portfolio, track performance, and diversify your holdings across various asset classes."),
        html.Li("Educational Resources: InvestIQ offers a wealth of educational resources, including tutorials, articles, and webinars, to help you enhance your investment knowledge and skills."),
        html.Li("Risk Management: InvestIQ helps you manage investment risk effectively with risk assessment tools, portfolio optimization strategies, and dynamic asset allocation."),
        html.Li("Community Engagement: Join a vibrant community of investors on InvestIQ to share insights, discuss investment strategies, and collaborate with like-minded individuals."),
    ], className='why-investiq-list'),
], className='why-investiq-container')
    elif pathname == '/':
        return html.Div([
        html.H1("Welcome to InvestIQ", className='home-header'),
        # Add home content here
        html.Div([
            html.H2("Features", className='features-header'),
            html.Div([
                html.Div([
                    html.Img(src=f"data:image/png;base64,{encoded_image22}", style={'width': '150px', 'height': '100px'}),
                    html.H5("Comprehensive Market Analysis"),
                    html.P("InvestIQ provides comprehensive market analysis tools, including real-time data, advanced charting, and customizable indicators, to help you analyze market trends and make informed decisions.")
                ], className='feature-box'),
                html.Div([
                    html.Img(src=f"data:image/png;base64,{encoded_image222}", style={'width': '150px', 'height': '100px'}),
                    html.H5("Portfolio Management"),
                    html.P("With InvestIQ, you can easily manage your investment portfolio, track performance, and diversify your holdings across various asset classes.")
                ], className='feature-box'),
                html.Div([
                    html.Img(src=f"data:image/png;base64,{encoded_imagee222}", style={'width': '150px', 'height': '100px'}),
                    html.H5("Educational Resources"),
                    html.P("InvestIQ offers a wealth of educational resources, including tutorials, articles, and webinars, to help you enhance your investment knowledge and skills.")
                ], className='feature-box'),
                html.Div([
                    html.Img(src=f"data:image/png;base64,{encoded_imagee22}", style={'width': '150px', 'height': '100px'}),
                    html.H5("Risk Management"),
                    html.P("InvestIQ helps you manage investment risk effectively with risk assessment tools, portfolio optimization strategies, and dynamic asset allocation.")
                ], className='feature-box'),
                html.Div([
                    html.Img(src=f"data:image/png;base64,{e}", style={'width': '150px', 'height': '100px'}),
                    html.H5("Community Engagement"),
                    html.P("Join a vibrant community of investors on InvestIQ to share insights, discuss investment strategies, and collaborate with like-minded individuals.")
                ], className='feature-box')
            ], className='feature-container')
        ], className='home-features'),
        html.Div([
            html.H2("How to Use InvestIQ", className='how-to-use-header'),
            html.Div([
                html.P("1. Navigate to the 'Top 50 Indian Stocks' page to view a list of the top 50 stocks in the Indian market."),
                html.P("2. Select any stock name to view detailed information and analysis for that stock."),
                html.P("3. Visit the 'AI Predictor' page to predict future stock prices using advanced machine learning algorithms."),
                html.P("4. Explore the 'Why InvestIQ?' page to learn about the features and benefits of using InvestIQ for your investment needs."),
                html.P("5. Get to know more about us on the 'About Us' page, where you can learn about our team and mission.")
            ], className='how-to-use-steps')
        ], className='how-to-use-container')
    ], className='home-container')
    else:
        return html.Div(
            [
                html.Div(
                    [
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
                                ), html.P("Hint: Select the start and end dates for the timeline you want to analyze.", style={'font-size': '14px', 'color': 'gray'}),
                                 html.Button("Submit", id="submit-button", n_clicks=0, className="submit-button",
                                 style={'border': '3px solid black'})
                            ],
                            className="input-container",
                            style={'border': '3px solid Black', 'padding': '60px',
                                   'background-image': f'url(data:image/png;base64,{encoded_imagee})', 'opacity': '1', 'transition': 'opacity 0.5s ease-in-out'}
                        ),
                        html.Hr(style={'padding': '5px'}, className='hhr'),
                        html.Div(
                            [
                                html.Div(
                                    children=[
                                        html.P("Stocks visualization and forecasting involve the graphical representation of historical stock price data and the prediction of future price movements. Visualization techniques include candlestick charts, line graphs, and scatter plots, which provide insights into past trends and patterns in stock prices. Forecasting, on the other hand, utilizes statistical models, machine learning algorithms, and artificial intelligence to analyze historical data and predict future stock prices. These forecasts assist investors, traders, and analysts in making informed decisions about buying, selling, or holding stocks by providing insights into potential future market trends and price movements.", className='para1'),
                                        html.P("Stock price prediction (SPP) is the process of forecasting future movements in the value of a particular stock or a basket of stocks. It involves analyzing historical price data, market trends, trading volumes, and various other factors to develop predictive models that can estimate the future price of a stock. SPP is essential for investors, traders, and financial analysts to make informed decisions about buying, selling, or holding stocks. Techniques such as machine learning, artificial intelligence, and statistical modeling are commonly employed in SPP to analyze large datasets and identify patterns that may indicate future price movements. Despite its challenges and inherent uncertainty, SPP plays a crucial role in financial markets by providing insights into potential investment opportunities and risks. ", className='para2'),
                                    ],
                                    className="para-container", id="paraaa", style={'opacity':'100%'}
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
                            style={'background-image': f'url(data:image/png;base64,{encoded_imageee})', 'opacity': '1', 'transition': 'opacity 0.5s ease-in-out'}
                        ),
                        # Disclaimer modal
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Disclaimer",style={'color':'Red'}),
                                dbc.ModalBody(
                                       children=[
                                     html.P("The information provided on this website is for educational and informational purposes only. It should not be considered as financial advice. Please consult with a qualified financial advisor before making any investment decisions."),
                                        html.P("Investing in stocks involves risk, including the potential loss of principal. Always do your own research and consult with a qualified investment professional before making any investment decisions."),
                                             ],style={'background-color': '#000000','color':'Red'}
                                ),
                                dbc.ModalFooter(
                                    dbc.Button("Close", id="close-disclaimer", className="ml-auto",style={'background-color':'Black' })
                                ),
                            ],
                            id="disclaimer-modal",
                            is_open=True  # Set to True to make it visible when the page loads
                        ),
                    ]
                )
            ]
        )

# Callback to update the stock chart based on user input
@app.callback(
    Output('stock-chart-container', 'children'), Output('paraaa', 'style'),
    [Input('submit-button', 'n_clicks')],
    [State('stock_input', 'value'),
     State('date-picker', 'start_date'),
     State('date-picker', 'end_date')]
)
def update_stock_chart(n_clicks, stock_input, start_date, end_date):
    if not n_clicks:
        raise PreventUpdate

    if not stock_input:
        return {},{'opacity':'100%'}

    try:
        start_date = dt.strptime(start_date.split('T')[0], '%Y-%m-%d').strftime('%d-%m-%Y')
        end_date = dt.strptime(end_date.split('T')[0], '%Y-%m-%d').strftime('%d-%m-%Y')

        df = equity_history(stock_input, 'EQ', start_date, end_date)

        if df.empty:
            raise Exception("No data found for the given stock code and date range.")

        fig = get_stock_graph(df, stock_input)  # Pass stock name to the function
        return dcc.Graph(id="Stock Chart", figure=fig, className='frame'),{'opacity':'0%'}

    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger", dismissable=True),{'opacity':'100%'}


# Callback to update the forecast graph based on user input
@app.callback(
    Output('forecast-graph-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('stock_input', 'value'),
     State('date-picker', 'start_date'),
     State('date-picker', 'end_date')]
)
def update_forecast_graph(n_clicks, stock_input, start_date, end_date):
    if not n_clicks:
        raise PreventUpdate

    if not stock_input:
        return {}

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
        return html.Div([
            html.P(f"An error occurred: {str(e)}")
        ])

# Callback to open/close the disclaimer modal
@app.callback(
    Output("disclaimer-modal", "is_open"),
    [Input("close-disclaimer", "n_clicks")],
    [State("disclaimer-modal", "is_open")],
)
def toggle_modal(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='8050')
