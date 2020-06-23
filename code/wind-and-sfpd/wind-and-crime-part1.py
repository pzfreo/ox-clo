from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row


from dateutil.parser import parse
from datetime import datetime

from numpy import array
from scipy import spatial


from pyspark.mllib.linalg import Vectors
from pyspark.mllib.stat import Statistics

#spark sql setup
conf = SparkConf().setAppName("wind-sfpd")
sc = SparkContext(conf=conf)
sqlc = SQLContext(sc)


# a useful function to parse and clean date/time

def date_and_hour(s):
    dt = parse(s.replace('?',' '))
    hour = dt.hour
    return dt.strftime("%Y-%m-%d")+":" +str(hour)


# start by reading the wind and temperature date

df = sqlc.read.format('csv').options(header='true').load('/home/oxclo/datafiles/wind2014/*.csv')

tidied = df.rdd.map(lambda r: Row(station = r.Station_ID, datehour =date_and_hour(r.Interval_End_Time), temp=r.Ambient_Temperature_Deg_C, wind=r.Wind_Velocity_Mtr_Sec)).toDF()

nonulls = tidied.filter(tidied.temp.isNotNull()).filter(tidied.wind.isNotNull())

numbered = nonulls.rdd.map(lambda row: Row(station=row.station, datehour=row.datehour, wind=float(row.wind), temp=float(row.temp))).toDF()

averages = numbered.groupBy(['station','datehour']).agg({'temp':'avg', 'wind':'avg'})

cleanedaverages = averages.rdd.map(lambda row: Row(station=row.station, datehour=row.datehour, temp=row['avg(temp)'], wind=row['avg(wind)'])).toDF()

print("wind and temp is now available in cleanedaverages")

cleanedaverages.show(10)
