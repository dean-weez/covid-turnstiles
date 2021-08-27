Code related to [dean.dog/subway-shutdown](http://dean.dog/subway-shutdown).

Plotting and data exploration all happens in the `analysis.ipynb` notebook, but there is some prep work to get the data ready to use.

1. `download.sh`: Pulls the raw data. There's a list of dates in here that controls what range to download.
2. `shard_stations.py`: Since most of the analysis will be done on a per-station basis, shuffle the date files into one file per station. There are a lot of rows in the raw data, so in the next steps being able to handle one station at a time makes things a little bit easier. NOTE: this script _appends_ data to files, so if you are re-running it be sure to rm any existing files first.
3. `preprocess.py`: Readings are counter values for each turnstile that are taken at potentially irregular intervals. For each turnstile, convert these counters into per-hour diffs (number of entries) and clean any weird values due to counters sometimes jumping forward or backwards. Aggregate turnstile-level counts to station-level counts.
4. `combine-stations.sh`: Combines processed station data files.

You may need to create the relevant directories for the above scripts to work.

`station_geo_lookup.csv` contains a mapping from station name to lat/lon and borough. It was somewhat cobbled together by hand, so no scripts to create this. It's _mostly_ correct, except for a couple cases where the station name was ambiguous and the location is either missing or has collapsed stations with the same name together.
