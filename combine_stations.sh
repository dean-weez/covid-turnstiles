#!\bin\bash

rm data/hourly_all.csv
cat data/station_hourly/* >> data/hourly_all.csv

rm data/daily_all.csv
cat data/station_daily/* >> data/daily_all.csv
