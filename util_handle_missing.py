
import pandas as pd
import os

provinces = ['Bangkok','Chanthaburi','Chiang Mai','Kanchanaburi','Khon Kaen','Songkhla']

def get_date_pm_missing(df):
    null_idx = df.loc[df['PM2.5'].isnull()].index
    return null_idx

def impute_Avg_by(df, method, null_idx):
    
    data = df.copy()

    if method == 'day':
        avg = df['PM2.5'].resample('D').mean()
        for e in null_idx:
            day = e.strftime("%Y-%m-%d")
            data.at[e,'PM2.5'] = avg.loc[day]

    elif method == 'week':
        avg = df['PM2.5'].resample('W').mean()
        avg.index = avg.index.strftime('%Y-%U')
        for e in null_idx:
            yr_week = e.strftime("%Y-%U")
            data.at[e,'PM2.5'] = avg.loc[yr_week]
    
    return data