import os
import csv

DATADIR = 'data'
RAWDIR = os.path.join(DATADIR, 'raw')
OUTDIR = os.path.join(DATADIR, 'station_raw')

def flush_stations(stations):
    for station, rows in stations.items():
        cleanname = ''.join(e for e in station if e.isalnum())
        fpath = os.path.join(OUTDIR, cleanname + '.csv')
        with open(fpath, 'a+') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

for fname in os.listdir(RAWDIR):
    fpath = os.path.join(RAWDIR, fname)
    stations = {}
    with open(fpath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row['DESC'] in ['RECOVER AUD', 'REGULAR']:
                continue
            outrow = [
                row['STATION'],
                row['STATION'] + row['UNIT'] + row['SCP'],
                row['DATE'],
                row['TIME'],
                row['ENTRIES']
            ]
            if row['STATION'] in stations:
                stations[row['STATION']] += [outrow]
            else:
                stations[row['STATION']] = [outrow]
    flush_stations(stations)
