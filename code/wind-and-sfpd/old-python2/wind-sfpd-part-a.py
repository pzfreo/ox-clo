from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext

from dateutil.parser import parse
from datetime import datetime

conf = SparkConf().setAppName("wind-sfpd")
sc = SparkContext(conf=conf)
sqlc = SQLContext(sc)

df = sqlc.read.format('com.databricks.spark.csv').\
options(header='true', inferschema='true').\
load('/home/oxclo/datafiles/wind2014/*.csv')

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

averaged = reduced.map(lambda ((s,d,h), (t,w,c)): ((s,d,h, t/c, w/c)))


 

