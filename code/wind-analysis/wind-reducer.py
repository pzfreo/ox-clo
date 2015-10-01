#! /usr/bin/env python
import sys

speeds = { "N": 0.0, "NE": 0.0, "E": 0.0, "SE":0.0, "S":0.0, "SW":0.0, "W":0.0, "NW":0.0}
counts = { "N": 0.0, "NE": 0.0, "E": 0.0, "SE":0.0, "S":0.0, "SW":0.0, "W":0.0, "NW":0.0}


for line in sys.stdin:
    try:

      line = line.strip()
      direction, count, speed = line.split('\t')

      count = int(count)
      speed = float(speed)

      counts[direction] += count
      speeds[direction] += speed
    
    except ValueError:
      pass

for k, v in counts.iteritems():
    average = speeds[k]/v
    result = [ k, str(average)]
    print('\t'.join(result))
      

