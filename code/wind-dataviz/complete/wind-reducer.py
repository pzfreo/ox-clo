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

data = dict(stations=list(), averages=list())

for k, v in counts.iteritems():
    average = speeds[k]/v
    result = [ k, str(average)]
    print('\t'.join(result))
    data['stations'] = k
    data['averages'] = average

from bokeh.charts import Bar
from bokeh.io import show
p = Bar(data, 'stations', values='speeds', title="Average wind speeds", width=400, height=400)
show(p)
