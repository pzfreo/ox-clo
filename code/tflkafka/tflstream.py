import sys
import json
from datetime import datetime
from dateutil.parser import parse
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


# Some useful stuff
zkQuorum = "kafka.freo.me:2181"
cpDir = "/home/oxclo/cp"

def update(ds,state):
    #   The ds is a dstream of new data (from MQTT)
    #   Each entry is a dictionary with keys: trainNumber, stationId, expArrival (plus others)
    #   The state is the previously calculated state
    #   In this case a dictionary of train -> (station, expected time, delayed)
    #   If the station has changed we set delayed false and update expected time
    #   if the station is the same, we check the current expected time against the previous
    #   and mark delayed if it has extended
    if state==None:
        state = dict()
    else:
        for current in ds:
            trainNumber = current['trainNumber']
            stationId = current['stationId']
            exp = parse(current['expArrival'])
            if trainNumber in state.keys():
                old = state[trainNumber]
                print old
                if old['stationId'] != stationId: 
                    state[trainNumber] = dict(stationId = stationId, expArrival = exp, delayed = False, delay = 0)
                else:
                    delay = exp-old['expArrival']
                    delay = delay.seconds
                    if (delay > 60): #anything less that a minute is not "delayed"
                        state[trainNumber] = dict(stationId = stationId, expArrival = exp, delayed = True, delay = delay)
            else:
                state[trainNumber] = dict(stationId = stationId, expArrival = exp, delayed = False, delay = 0)
    return state 


def printit(s): print s

sc = SparkContext(appName="TFLStreaming")
ssc = StreamingContext(sc, 5) # batch interval 5 sec
ssc.checkpoint(cpDir)
topic = "tfl"

lines = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming", { topic: 1} )
#lines.pprint();
windowed = lines.window(600,5) # look at the last 10 minutes worth with a sliding window of 5 seconds
dicts = lines.map(lambda (ignore,element): json.loads(element)) # convert from json into a Python dict
mapped = dicts.map(lambda d: (d['trainNumber'],d)) # make the train number the key
ds = mapped.updateStateByKey(update) # compare against previous data
info = ds.filter(lambda (r, d): bool(d)) # ignore if there is no previous data
# the state from the update is a dict (train -> info)
# this is then mapped with a key so we have (train, (train->info))
# so let's get rid of the redundancy
unpack = info.map(lambda (r, d): (r, d[r]))
# now let's swap this over so that the key is whether the train is delayed or not, and assign a count
remap = unpack.map(lambda (r,d): ('delayed', 1) if d['delayed'] else ('ontime', 1))
#now let's count the results with a reducer
counts = remap.reduceByKey(lambda a,b: a+b)
# and print the result to the console
counts.pprint() 

#start the processing
ssc.start()
# keep running forever (until Ctrl-C)
ssc.awaitTermination()
