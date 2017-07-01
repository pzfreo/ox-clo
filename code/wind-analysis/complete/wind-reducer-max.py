#! /usr/bin/env python
import sys

speeds = dict()


# counts = dict()
# need this for extension

for line in sys.stdin:
    try:

      line = line.strip()
      station, speed = line.split('\t')

      speed = float(speed)
	  # Add code here to use the data
      if station in speeds:
      	if speeds[station] < speed:
       		speeds[station] = speed
      else:
      	speeds[station] = speed
    
    except ValueError:
      pass


for k, v in speeds.iteritems():
	result = [k,str(v)]
	print ('\t'.join(result))

	# add code here to output the results