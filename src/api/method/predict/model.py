import datetime
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures


def data_model(initial_data):
    """Моделирование цены акций эмитента."""
    initial_data['dayofyear'] = initial_data['dates'].dt.dayofyear
    data_train = initial_data[initial_data['dates'] < initial_data['dates'][int(initial_data['dates'].shape[0] / 2)]]
    data_test = initial_data[initial_data['dates'] >= initial_data['dates'][int(initial_data['dates'].shape[0] / 2)]]

    x_train = pd.DataFrame()
    x_train['dayofyear'] = data_train['dates'].dt.dayofyear
    x_train['dayofyear'] = x_train[['dayofyear']].values
    y_train = data_train['CLOSE'].values

    x_test = pd.DataFrame()
    x_test['dayofyear'] = data_test['dates'].dt.dayofyear
    x_test['dayofyear'] = x_test[['dayofyear']].values
    y_test = data_test['CLOSE'].values

    now = datetime.datetime.now()
    days_delta = datetime.timedelta(days=-5)
    next_date = now - days_delta
    data_future = pd.DataFrame()
    data_future['dates'] = pd.date_range(start=now.strftime('%Y-%m-%d'), end=next_date.strftime('%Y-%m-%d'))
    data_future['dayofyear'] = data_future['dates'].dt.dayofyear
    x_future = pd.DataFrame()
    x_future['dayofyear'] = data_future['dates'].dt.dayofyear
    x_future['dayofyear'] = x_future[['dayofyear']].values

    collect_all_rez = []
    for poly_order in range(1, 5):
        collect_rez = []
        poly_reg = PolynomialFeatures(degree=poly_order)
        x_poly = poly_reg.fit_transform(x_train)
        model = LinearRegression()
        model.fit(x_poly, y_train)

        pred_train = model.predict(poly_reg.fit_transform(x_train))
        pred_test = model.predict(poly_reg.fit_transform(x_test))
        pred_future = model.predict(poly_reg.fit_transform(x_future))

        train_mean = mean_squared_error(y_train, pred_train)
        test_mean = mean_squared_error(y_test, pred_test)
        collect_rez.append(pred_future)
        collect_rez.append(abs(train_mean - test_mean))
        collect_all_rez.append(collect_rez)

    collect_mean = [(i[1]) for i in collect_all_rez]
    index_min_val = np.argmin(collect_mean)
    out_data = pd.DataFrame()
    out_data['dates'] = data_future['dates']
    out_data['future_price'] = collect_all_rez[index_min_val][0]
    return out_data
