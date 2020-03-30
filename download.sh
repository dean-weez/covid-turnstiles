#!/bin/bash

PREFIX="http://web.mta.info/developers/data/nyct/turnstile/turnstile_"
SUFFIX=".txt"
DIR="./data/raw"

declare -a dates=(
    "200328"
    "200321"
    "200314"
    "200307"
    "200229"
    "200222"
    "200215"
    "200208"
)

for date in "${dates[@]}"
do
    path=$DIR/$date$SUFFIX
    url=$PREFIX$date$SUFFIX
    curl $url -o $path
done