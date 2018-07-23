#!/bin/bash
currentDateTs=$(date -j -f "%Y-%m-%d" $1 "+%s")
endDateTs=$(date -j -f "%Y-%m-%d" $2 "+%s")
offset=86400

while [ "$currentDateTs" -le "$endDateTs" ]
do
  date=$(date -j -f "%s" $currentDateTs "+%Y-%m-%d")
  echo $date
  currentDateTs=$(($currentDateTs+$offset))
done