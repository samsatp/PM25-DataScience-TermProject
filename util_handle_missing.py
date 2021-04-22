
import pandas as pd
import os

provinces = ['Bangkok','Chanthaburi','Chiang Mai','Kanchanaburi','Khon Kaen','Songkhla']

def get_date_pm_missing(data):
    missing = dict()
    for province in provinces:
        null_idx = data[province]['PM2.5'].isnull()
        missing[province] = data[province].loc[null_idx].index

        print(f'{province} has {len(missing[province])} missing values')
    return missing

def impute_Avg_by(data, method, missing):
    for province in provinces:

        if method == 'day':
            avg = data[province]['PM2.5'].resample('D').mean()
            
            for e in missing[province]:
                day = e.strftime("%Y-%m-%d")
                data[province].at[e,'PM2.5'] = avg.loc[day]

        elif method == 'week':
            avg = data[province]['PM2.5'].resample('W').mean()
            avg.index = avg.index.strftime('%Y-%U')

            for e in missing[province]:
                yr_week = e.strftime("%Y-%U")
                data[province].at[e,'PM2.5'] = avg.loc[yr_week]
    return data