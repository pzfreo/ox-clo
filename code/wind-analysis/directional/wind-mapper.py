#! /usr/bin/env python
import sys
for line in sys.stdin:
    line = line.strip()
    unpacked = line.split(",")
    try:
       Station_ID,Station_Name,Location_Label,Interval_Minutes,Interval_End_Time,vel,Wind_Direction_Variance_Deg,wdd_string,Ambient_Temperature_Deg_C,Global_Horizontal_Irradiance = line.split(",")
    except ValueError:
       pass

    if (Station_ID=="Station_ID"): continue

    wdd = 0
    try: 
   	 wdd = float(wdd_string)
    except ValueError:
         # count was not a number, so silently discard this item
         pass

    if (wdd < 22.5):
	direction = "N"
    elif (wdd < 67.5):
        direction = "NE"
    elif (wdd < 112.5):
        direction = "E"
    elif (wdd < 157.5):
        direction = "SE"
    elif (wdd < 202.5):
 	direction = "S"
    elif (wdd < 247.5):
	direction = "SW"
    elif (wdd < 292.5):
 	direction = "W"
    elif (wdd < 337.5):
	direction = "NW"
    else:
 	direction = "N"

    results = [direction, "1",  vel] #fixed VALUE of string "1", KEY is either TRUE or FALSE
    print("\t".join(results)) #dump line by line to stdout, this is different from KEY,ITERABLE[VALUES] format of java
