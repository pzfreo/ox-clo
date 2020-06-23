from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext

from dateutil.parser import parse
from datetime import datetime
from scipy import spatial
from numpy import array

conf = SparkConf().setAppName("wind-sfpd")
sc = SparkContext(conf=conf)
sqlc = SQLContext(sc)

df = sqlc.read.format('com.databricks.spark.csv').\
options(header='true', inferschema='true').\
load('file:///home/oxclo/datafiles/wind2014/*.csv')

def date_and_hour(s):
    dt = parse(s.replace('?',' '))
    hour = dt.hour
    return (dt.strftime("%Y-%m-%d"), hour)

tidied = df.rdd.map(lambda r: (r.Station_ID, date_and_hour(r.Interval_End_Time), \
(r.Ambient_Temperature_Deg_C, r.Wind_Velocity_Mtr_Sec)))

tidier = tidied.map(lambda (s, (d,h), (t,w)): ((s,d,h),(t,w)))

filtered = tidier.filter( lambda ((s,d,h),(t,w)):  not (t==0.0 and w==0.0))

filter2 = filtered.filter(lambda ((s,d,h),(t,w)):  bool(t) and  bool(w))

mapped = filter2.map( lambda ((s,d,h),(t,w)): ((s,d,h), (t,w,1)))

reduced = mapped.reduceByKey( lambda (t1,w1,c1), (t2,w2,c2): (t1+t2,w1+w2,c1+c2))

windaveraged = reduced.map(lambda ((s,d,h), (t,w,c)): ((s,d,h), (t/c, w/c)))


df2 = sqlc.read.format('com.databricks.spark.csv').\
options(header='true', inferschema='true').\
load('file:///home/oxclo/datafiles/incidents/sfpd.csv.gz')


fixed = df2.rdd.map(lambda r: (parse(r.Date+" "+r.Time), [r.Y,r.X]))

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
incidentsreduced = counted.reduceByKey(lambda a,b: a+b)

joined = windaveraged.join(incidentsreduced)


from pyspark.mllib.linalg import Vectors
from pyspark.mllib.stat import Statistics

vecs = joined.map(lambda ((s,d,h),((t,w),i)): Vectors.dense([t,w,i]))
print(Statistics.corr(vecs))


 

