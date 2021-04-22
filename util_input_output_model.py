from datetime import timedelta
import numpy as np
import pandas as pd
from collections import defaultdict
from sklearn.preprocessing import MinMaxScaler

provinces = ['Bangkok','Chanthaburi','Chiang Mai','Kanchanaburi','Songkhla']

def prepare_train_data(timesteps):
    path = f'./data/Train/fire_integrated/'
    data = {}

    X = defaultdict(lambda: list())
    Y = defaultdict(lambda: list())

    hour_step = timedelta(hours=timesteps-1)

    # Time we have to forecast
    predict_at = pd.date_range("2016-03-04 00:00:00", "2019-03-17 23:00:00", freq='6H')

    for province in provinces:
        # Read preprocessed data
        df = pd.read_csv(path+f'{province}_fire_integrated.csv', index_col=0, parse_dates=True)
        data[province] = df

        # Create Input & Output of model
        for base in predict_at:

            if base-hour_step not in df.index : continue
            x = df.loc[base-hour_step: base].drop(['PM2.5'], axis=1)

            till = base+timedelta(hours=72)
            if till not in df.index: break
            y = df.loc[base+timedelta(hours=1): till, ['PM2.5']]

            X[province].append(x)
            Y[province].append(y)

    return data, X, Y

def prepare_test_data(Train_data, timesteps):
    path = "./data/Test/fire_integrated/"
    data = {}
    
    predict_at = pd.date_range("2019-3-18 12:00:00", '2020-03-15 18:00:00', freq='6H')

    hour_step = timedelta(hours= timesteps-1)
    X = defaultdict(lambda: list())
    Y = defaultdict(lambda: list())
    i=0
    for province in provinces:
        df = pd.read_csv(path+f'{province}_fire_integrated.csv', index_col=0, parse_dates=True)
        data[province] = df

        for base in predict_at:
            
            if base-hour_step < df.index[0]:
                dif = int((df.index[0] - (base-hour_step)).total_seconds()//3600)
                if i<4:
                    print('dif :', dif)
                    print(df.index[0])
                    print('base =', base)
                    i+=1
                a = Train_data[province].iloc[-dif:]
                b = df.loc[:base]
                x = a.append(b).drop(['PM2.5'], axis=1)
            else:
                x = df.loc[base-hour_step: base].drop(['PM2.5'],axis=1)

            till = base+timedelta(hours=72)
            y = df.loc[base+timedelta(hours=1): till, ['PM2.5']]

            X[province].append(x)
            Y[province].append(y)
    return data, X, Y


def scale_data(X, Y, data):
    x_scalers, y_scalers = {}, {}

    X_scaled = defaultdict(lambda: list())
    Y_scaled = defaultdict(lambda: list())

    for province in provinces:
        # Standardize x, y
        x = data[province].drop(['PM2.5'], axis=1)
        y = data[province][['PM2.5']]

        x_scaler = MinMaxScaler().fit(x)
        y_scaler = MinMaxScaler().fit(y)

        # Save the scaler for later use
        x_scalers[province] = x_scaler
        y_scalers[province] = y_scaler

        # Scale the data
        for e in X[province]:
            X_scaled[province].append(x_scaler.transform(e))
            
        for e in Y[province]:
            Y_scaled[province].append(y_scaler.transform(e))
            
    
    return x_scalers, y_scalers, X_scaled, Y_scaled