#! /usr/bin/env python
import sys

speeds = dict()
counts = dict()

for line in sys.stdin:
    try:

      line = line.strip()
      station, speed = line.split('\t')

      speed = float(speed)
	  # Add code here to use the data

    
    except ValueError:
      pass

for k, v in counts.iteritems():
	# add code here to output the results
