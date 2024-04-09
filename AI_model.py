
def prediction(stocks, n_days):
    import dash
    from dash import dcc
    from dash import html as html
    from datetime import datetime as dt
    from nsepython import equity_history
    from dash.dependencies import Input, Output, State
    from dash.exceptions import PreventUpdate
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.express as px
    # model
    from sklearn.model_selection import train_test_split
    from sklearn.model_selection import GridSearchCV
    import numpy as np
    from sklearn.svm import SVR
    from datetime import date, timedelta

    #load the data
    st=(dt.today()-timedelta(days=100)).strftime("%d-%m-%Y")
    en=dt.today().strftime("%d-%m-%Y")
    df=equity_history(stocks,'EQ',st, en)
    df['CH_TIMESTAMP']=df.index

    days=list()
    for i in range(len(df.CH_TIMESTAMP)):
        days.append([i])

    #Splitting the dataset
    
    X= days
    Y=df['CH_CLOSING_PRICE']

    x_train, x_test, y_train,y_test= train_test_split(X,Y, test_size=0.25, shuffle=False)

    gsc=GridSearchCV(
        estimator=SVR(kernel='rbf'),
    param_grid={
        'C':[0.001,0.01,0.1,10,100,1000],
        'epsilon': [
            0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1, 1, 5, 10,50,100,150,1000],
            'gamma': [0.0001, 0.001, 0.005, 0.1, 1, 3, 5, 8, 40, 100, 1000]
            },
            cv=5,
            scoring='neg_mean_absolute_error',
            verbose=0,
            n_jobs=-1)
    
    grid_result=gsc.fit(x_train,y_train)
    best_params=grid_result.best_params_
    best_svr=SVR(kernel='rbf',
                 C=best_params["C"],
                 epsilon=best_params["epsilon"],
                 gamma=best_params["gamma"],
                 max_iter=-1)
    
    # Support Vector Regression Models

    # RBF model
    #rbf_svr = SVR(kernel='rbf', C=1000.0, gamma=4.0)
    rbf_svr = best_svr

    rbf_svr.fit(x_train, y_train)

    n_days=int(n_days)
    output_days = list()
    for i in range(1, n_days+1):
        output_days.append([i + x_test[-1][0]])

    dates = []
    current = date.today()
    for i in range(n_days):
        current += timedelta(days=1)
        dates.append(current)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,  # np.array(ten_days).flatten(), 
            y=rbf_svr.predict(output_days),
            mode='lines+markers',
            name='data'))
    fig.update_layout(
        title="Predicted Close Price of next " + str(n_days) + " days for "+stocks,
        xaxis_title="Date",
        yaxis_title="Closed Price",
        # legend_title="Legend Title",
    )

    return fig