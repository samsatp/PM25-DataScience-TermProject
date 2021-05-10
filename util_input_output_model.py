from datetime import timedelta
import numpy as np
import pandas as pd
from collections import defaultdict
from sklearn.preprocessing import MinMaxScaler

provinces = ['Bangkok','Chanthaburi','Chiang Mai','Kanchanaburi','Songkhla','Khon Kaen']

def prepare_train_data(timesteps, feature_used:list):
    # Train data: from 2016-03-03 to 2019-03-17
    path = f'./data/Train/imputed_fired/'
    data = {}

    X = defaultdict(lambda: list())
    Y = defaultdict(lambda: list())

    hour_step = timedelta(hours=timesteps-1)

    # Time we have to forecast
    predict_at = pd.date_range("2016-03-04 00:00:00", "2019-03-17 23:00:00", freq='6H')

    for province in provinces:
        # Read preprocessed data
        df = pd.read_csv(path+f'{province}_imputed_fired.csv', index_col=0, parse_dates=True)[feature_used]
        data[province] = df

        # Create Input & Output of model
        for base in predict_at:

            if base-hour_step not in df.index : continue
            x = df.loc[base-hour_step: base] #.drop(['PM2.5'], axis=1)

            till = base+timedelta(hours=72)
            if till not in df.index: break
            y = df.loc[base+timedelta(hours=1): till, ['PM2.5']]

            X[province].append(x)
            Y[province].append(y)

    return data, X, Y


## DEPRECATED
'''
def prepare_test_data(Train_data, timesteps, feature_used:list):
    path = "./data/Test/imputed_fired/"
    data = {}

    start_at = pd.Timestamp("2019-3-18 12:00:00")

    hour_step = timedelta(hours= timesteps-1)
    X = defaultdict(lambda: list())
    Y = defaultdict(lambda: list())

    for province in provinces:
        
        testdf = pd.read_csv(path+f'{province}_imputed_fired.csv', index_col=0, parse_dates=True)[feature_used]
        
        df = Train_data[province].append(testdf)

        while start_at + timedelta(73) < df.index[-1]:
            if (start_at not in testdf.index) or (start_at.hour not in [0,6,12,18]):
                start_at+=timedelta(hours=1)
                continue
            
            idx = list(df.index).index(start_at)

            ## X
            x = df.iloc[idx-timesteps+1:idx+1]
            
            ## Y
            y = df.iloc[idx+1:idx+73, [0]]

            X[province].append(x)
            Y[province].append(y)
            start_at+=timedelta(hours=1)


    return data, X, Y       
'''     
'''
        for base in predict_at:
            
            if base-hour_step < df.index[0]:
                dif = int((df.index[0] - (base-hour_step)).total_seconds()//3600)

                a = Train_data[province].iloc[-dif:]
                b = df.loc[:base]
                x = a.append(b) #.drop(['PM2.5'], axis=1)
            else:
                x = df.loc[base-hour_step: base] #.drop(['PM2.5'],axis=1)

            till = base+timedelta(hours=72)
            y = df.loc[base+timedelta(hours=1): till, ['PM2.5']]

            X[province].append(x)
            Y[province].append(y)
'''
    


def scale_data(X, Y, data):
    x_scalers, y_scalers = {}, {}

    X_scaled = defaultdict(lambda: list())
    Y_scaled = defaultdict(lambda: list())

    for province in provinces:
        # Standardize x, y
        x = data[province] #.drop(['PM2.5'], axis=1)
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

def prepare_new_test(Train_data, timesteps, feature_used:list):
    path = "./data/new test/"
    data = {}

    hour_step = timedelta(hours= timesteps-1)
    X = defaultdict(lambda: list())
    Y = defaultdict(lambda: list())

    for province in provinces:
        
        testdf = pd.read_csv(path+f'{province}_new_test.csv', index_col=0, parse_dates=True)[feature_used]
        
        idx = testdf.iloc[:-72].index
        predict_at = idx[idx.hour.isin([6,12,18,0])]
        
        df = Train_data[province].append(testdf)

        for base in predict_at:
            
            i = list(df.index).index(base)

            ## X
            x = df.iloc[i-timesteps+1:i+1]
            
            ## Y
            y = df.iloc[i+1:i+73, [0]]

            X[province].append(x)
            Y[province].append(y)

    return data, X, Y

## DEPRECATED
'''
def quick_eval(path, province):
    m = tf.keras.models.load_model(path)
    print(f"province: {province}")

    x_eval, y_eval = x_[province]['Test'], y_[province]['Test']
    m.evaluate(x_eval, y_eval)

    pred = m(x_eval)
    rmse = []

    for i in range(len(pred)):
        p = y_train_scalers[province].inverse_transform(pred[i].numpy().reshape((-1,1)))
        y_t = Y_test[province][i].values
        rmse.append(np.sqrt(mse(p, y_t)))
    return np.mean(rmse)
'''