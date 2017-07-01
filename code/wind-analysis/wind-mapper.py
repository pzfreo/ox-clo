#! /usr/bin/env python
import sys
# we need to use CSV reader because some files have "," so splitting on , doesn't work
import csv
for line in sys.stdin:
  try:	
    line = line.strip()
    for unpacked in csv.reader([line]): 
      stationid,name,location,interval,time,vel,direction_variance,wdd,temp,irradiance = unpacked
      vel = float(vel)
      
      # add your code to output <K,V> here
      
      
      
  except ValueError:
    pass
