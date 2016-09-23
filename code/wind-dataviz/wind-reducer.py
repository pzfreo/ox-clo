#! /usr/bin/env python
import sys

speeds = dict()
counts = dict()

for line in sys.stdin:
    try:

      line = line.strip()
      station, speed = line.split('\t')

      speed = float(speed)

      if station in counts.keys(): 
        counts[station] += 1
        speeds[station] += speed
      else:
        counts[station] = 1
        speeds[station] = speed
    
    except ValueError:
      pass

# Populate this dictionary with data to use in your chart
data = dict(stations=list(), averages=list())

for k, v in counts.iteritems():
    average = speeds[k]/v
    result = [ k, str(average)]
    print('\t'.join(result))

# Put your bokeh code here to render your chart.
# Make sure it's outside of the for-loops!
