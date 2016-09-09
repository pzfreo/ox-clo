import time
import httplib2
from urllib import urlencode
import json
from kafka import KafkaProducer

def call_get_arrivals(line):

    h = httplib2.Http(disable_ssl_certificate_validation=True)
#    h.add_credentials(intro_username, intro_password)
    resp, content = h.request("https://api.tfl.gov.uk/Line/"+line+"/Arrivals")

#    print resp            
    try:
       response=json.loads(content)
       for i in response:
         line = i['lineName']
         trainNumber = i['vehicleId']
         stationId = i['destinationNaptanId']
         stationName = i['destinationName']
         expArrival = i['expectedArrival']
         timestamp = i['timestamp']
         ttl = i['timeToLive']
         data = dict(line=line, trainNumber = trainNumber, stationId = stationId, stationName=stationName, timestamp=timestamp, expArrival = expArrival, ttl = ttl)
         #print data
         producer.send("tfl", json.dumps(data))
    except Exception as inst:
       pass
     


lines = ["victoria","circle","district","northern","jubilee","piccadilly","metropolitan","bakerloo","central" ]
time.sleep(30) #wait for kafka
producer = KafkaProducer(bootstrap_servers='kafka.freo.me:9092')

while 1==1:
    for line in lines:
      call_get_arrivals(line)
      time.sleep(1)
