#! /usr/bin/env python
import sys
import csv
for line in sys.stdin:
  try:	
    line = line.strip()
    for unpacked in csv.reader([line]):
      stationid,name,location,interval,time,vel,direction_variance,wdd,temp,irradiance = unpacked
      vel = float(vel) 
      results = [stationid,  str(vel)] 
      print("\t".join(results)) 
      
  except:
    pass
