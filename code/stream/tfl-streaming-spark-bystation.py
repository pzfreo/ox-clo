import sys
import json
from datetime import datetime
from dateutil.parser import parse
import paho.mqtt.client as mqtt

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.mqtt import MQTTUtils


# Some useful stuff
brokerHost = "mqtt.freo.me"
brokerPort = 1883
brokerUrl = "tcp://"+brokerHost+":"+str(brokerPort)
listenTopic = "/tfl/"
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



sc = SparkContext(appName="TFLStreaming")
ssc = StreamingContext(sc, 5) # batch interval 5 sec
ssc.checkpoint(cpDir)

lines = MQTTUtils.createStream(ssc, brokerUrl, listenTopic)
windowed = lines.window(600,5) # look at the last 10 minutes worth with a sliding window of 5 seconds

dicts = lines.map(lambda js: json.loads(js)) # convert from json into a Python dict
mapped = dicts.map(lambda d: (d['trainNumber'],d)) # make the train number the key
ds = mapped.updateStateByKey(update) # compare against previous data
info = ds.filter(lambda (r, d): bool(d)) # ignore if there is no previous data
# the state from the update is a dict (train -> info)
# this is then mapped with a key so we have (train, (train->info))
# so let's get rid of the redundancy
unpack = info.map(lambda (r, d): (r, d[r]))
# now let's swap this over so that the key is whether the train is delayed or not, and assign a count

ontime = unpack.filter(lambda (r,d): not d['delayed'])
remap = ontime.map(lambda (r,d): (d['stationId'],1))
#now let's count the results with a reducer
counts = remap.reduceByKey(lambda a,b: a+b)
# and print the result to the console
counts.pprint() 

#start the processing
ssc.start()
# keep running forever (until Ctrl-C)
ssc.awaitTermination()