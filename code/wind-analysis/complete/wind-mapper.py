#! /usr/bin/env python
import sys
import csv
for line in sys.stdin:
  try:	
    line = line.strip()
    for unpacked in csv.reader([line]):
      Station_ID,Station_Name,Location_Label,Interval_Minutes,Interval_End_Time,vel,Wind_Direction_Variance_Deg,wdd_string,Ambient_Temperature_Deg_C,Global_Horizontal_Irradiance = unpacked
      vel = float(vel)
      results = [Station_ID,  str(vel)] 
      print("\t".join(results)) #dump line by line to stdout, this is different from KEY,ITERABLE[VALUES] format of java

  except:
    pass
