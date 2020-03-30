import pandas as pd
import numpy as np
from datetime import datetime
import os

DATADIR = 'data'
RAWDIR = os.path.join(DATADIR, 'station_raw')
HOURDIR = os.path.join(DATADIR, 'station_hourly')
DAYDIR = os.path.join(DATADIR, 'station_daily')

def process_station(fname):
    colnames = ['station', 'turnstile', 'date', 'time', 'entries']
    data = pd.read_csv(os.path.join(RAWDIR, fname), names=colnames)
    data['ts'] = pd.to_datetime(data['date']+' ' +data['time'], format='%m/%d/%Y %H:%M:%S')
    data.drop(columns=['date', 'time'], inplace=True)
    data.set_index('ts', inplace=True)

    def make_diffs(df):
        df2 = df.resample('H').max().interpolate().ffill()
        df2['diff'] = df2['entries'] - df2['entries'].shift(1)
        df2.loc[df2['diff'] < 0, 'diff'] = np.nan
        df2.loc[df2['diff'] > 10000, 'diff'] = np.nan
        df3 = df2.interpolate().dropna() # re-interpolate bad values, drop remaining na
        return df3

    diffs = data.groupby(['station', 'turnstile'], group_keys=False).apply(make_diffs)

    stations_hourly = diffs.groupby(['station', 'ts'])['diff'].sum().reset_index()
    stations_hourly.to_csv(os.path.join(HOURDIR, fname), index=False, header=False)

    stations_daily = stations_hourly.groupby(['station', pd.Grouper(key='ts', freq='D')]).sum().reset_index()
    stations_daily.to_csv(os.path.join(DAYDIR, fname), index=False, header=False)

for fname in os.listdir(RAWDIR):
    process_station(fname)
    print('Processed %s'  % fname)
