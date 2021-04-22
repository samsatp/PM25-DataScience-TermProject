import numpy as np 
import pandas as pd 
import os
provinces = ['Khon Kaen','Chiang Mai','Chanthaburi','Bangkok','Kanchanaburi','Songkhla']
dest_url = './extracted/'

def get_target_df(province, subset):
    
    # If it's a test set
    if subset == 'Test':
        target_url = f'../{province}/Test/{province}.csv'
        return pd.read_csv(target_url, index_col=0)

    # If it's a train set
    target_url = f'../{province}/Train/{province}.txt'
    with open(target_url, 'r') as f:
        for i, line in enumerate(f):
            if i==9:
                cols = line.strip().split(', ')
                break
            
    target_df = pd.read_csv(target_url, sep='\t', skiprows=10, header=None)
    target_df.columns = cols
    target_df.iloc[:,:4] = target_df.iloc[:,:4].applymap(str)
    target_df['Date'] = pd.to_datetime({'year': target_df['% Year'], 
                                        'month': target_df['Month'], 
                                        'day':target_df['Day'],
                                        'hour': target_df['UTC Hour']})
    target_df = target_df[['Date','PM2.5']].set_index('Date')
    return target_df

def get_df(measure, province, subset):
    url = f'../{province}/{subset}/3H_{measure}_{province}.csv'
    return pd.read_csv(url, parse_dates=['datetime'], index_col='datetime')


def join_pm_wind_temp(subset):
    wind_temp = {}
    target = {}
    for p in provinces:
        target_p = pd.read_csv(dest_url+'/{}/{}_target.csv'.format(subset,p), 
                        parse_dates=True, index_col=0)
        wind_p = pd.read_csv(dest_url+'/{}/{}_wind.csv'.format(subset,p), 
                        parse_dates=['datetime'], index_col='datetime').drop(['lat','long'], axis=1)
        temp_p = pd.read_csv(dest_url+'/{}/{}_temp.csv'.format(subset,p), 
                        parse_dates=['datetime'], index_col='datetime').drop(['lat','long'], axis=1)

        wind_temp[p] = wind_p.merge(temp_p, left_index=True, right_index=True, how='inner')
        target[p] = target_p.merge(wind_temp[p], left_index=True, right_index=True, how='left')
    
    return wind_temp, target