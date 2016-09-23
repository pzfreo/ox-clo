#! /usr/bin/env python
import sys
import csv

x = list()
y = list()

for i, line in enumerate(sys.stdin):
  try:	
    line = line.strip()
    for unpacked in csv.reader([line]):
      stationid,name,location,interval,time,vel,direction_variance,wdd,temp,irradiance = unpacked
      vel = float(vel) 
      results = [stationid,  str(vel)] 
      print("\t".join(results)) 

      x.append(i)
      y.append(vel)
      
  except:
    pass

from bokeh.plotting import figure
from bokeh.io import show
p = figure(title="Wind speeds", x_axis_label='x', y_axis_label='y')
p.line(x, y, legend="Mtr per sec.", line_width=2)
show(p)

