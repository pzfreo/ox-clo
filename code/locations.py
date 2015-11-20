from pyspark.sql import SQLContext
sqlc = SQLContext(sc)

from dateutil.parser import parse
from datetime import datetime
from scipy import spatial
from numpy import array



geoindex = spatial.KDTree(array( \
[[37.7816834,-122.3887657],\
[37.7469112,-122.4821759],\
[37.7411022,-120.804151],\
[37.4834543,-122.3187302],\
[37.7576436,-122.3916382],\
[37.7970013,-122.4140409],\
[37.748496,-122.4567461],\
[37.7288155,-122.4210133],\
[37.5839487,-121.9499339],\
[37.7157156,-122.4145311],\
[37.7329613,-122.5051491],\
[37.7575891,-122.3923824],\
[37.7521169,-122.4497687]]))
locations = ["SF18", "SF04", "SF15", "SF17", "SF36", "SF37", "SF07", "SF11", "SF12", "SF14", "SF16", "SF19", "SF34"]

# locate([37.7736224122729, -122.463749926391])

df = sqlc.read.format('com.databricks.spark.csv').\
options(header='true', inferschema='true').\
load('/home/oxclo/datafiles/incidents/sfpd.csv.gz')


fixed = df.rdd.map(lambda r: (parse(r.Date), [r.Y,r.X]))

only2014 = fixed.filter(lambda (d,l): d.year == 2014)

remapped = only2014.map(lambda (d,loc): (d.strftime("%Y-%m-%d"), d.hour, loc))



def locate(l,index,locations):
	distance,i = index.query(l)
	return locations[i]

# 
located = remapped.map(lambda (d, h, l): (locate(l, \
spatial.KDTree(array( \
[[37.7816834,-122.3887657],\
[37.7469112,-122.4821759],\
[37.7411022,-120.804151],\
[37.4834543,-122.3187302],\
[37.7576436,-122.3916382],\
[37.7970013,-122.4140409],\
[37.748496,-122.4567461],\
[37.7288155,-122.4210133],\
[37.5839487,-121.9499339],\
[37.7157156,-122.4145311],\
[37.7329613,-122.5051491],\
[37.7575891,-122.3923824],\
[37.7521169,-122.4497687]])),
["SF18", "SF04", "SF15", "SF17", "SF36", "SF37",\
"SF07", "SF11", "SF12", "SF14", "SF16", "SF19", "SF34"] ),d,h))


counted = located.map(lambda (l,d,h): ((l,d,h),1))
reduced = counted.reduceByKey(lambda a,b: a+b)




