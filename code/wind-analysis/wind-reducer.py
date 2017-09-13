#! /usr/bin/env python
import sys

speeds = dict()
# for the extension we will need another dictionary
# counts = dict()

for line in sys.stdin:
    try:

      line = line.strip()
      station, speed = line.split('\t')

      speed = float(speed)
	  # Add code here to use the data

    
    except ValueError:
      pass

for k, v in speeds.iteritems():
	# add code here to output the results
