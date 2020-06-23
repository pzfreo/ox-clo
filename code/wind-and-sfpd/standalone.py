from datetime import datetime

from dateutil.parser import parse
from numpy import array
from scipy import spatial

from pyspark import SparkConf, SparkContext
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.stat import Statistics
from pyspark.sql import Row, SQLContext

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

# now read the incident data and clean 

idf = sqlc.read.format('csv').options(header='true').load('/home/oxclo/datafiles/incidents/sfpd.csv')

withyx2014 = idf.filter(idf.X.isNotNull()).filter(idf.Y.isNotNull()).filter(idf.Date.contains('2014'))

tidy = withyx2014.rdd.map(lambda row: Row(datehour = date_and_hour(row.Date+" "+row.Time),yx=[float(row.Y),float(row.X)])).toDF()

# need to associate incidents with nearest weather station

def locate(l,index,locations):
    distance,i = index.query(l)
    return locations[i]

def map_yx_to_station(yx):
    return locate(yx,         spatial.KDTree(array(         [[37.7816834,-122.3887657],        [37.7469112,-122.4821759],        [37.7411022,-120.804151],        [37.4834543,-122.3187302],        [37.7576436,-122.3916382],        [37.7970013,-122.4140409],        [37.748496,-122.4567461],        [37.7288155,-122.4210133],        [37.5839487,-121.9499339],        [37.7157156,-122.4145311],        [37.7329613,-122.5051491],        [37.7575891,-122.3923824],        [37.7521169,-122.4497687]])),
        ["SF18", "SF04", "SF15", "SF17", "SF36", "SF37",\
        "SF07", "SF11", "SF12", "SF14", "SF16", "SF19", "SF34"] )


                  
withstations = tidy.rdd.map(lambda row: Row(station=map_yx_to_station(row.yx), datehour=row.datehour)).toDF()

withstations.registerTempTable('stationincidents')
incidentcount = sqlc.sql("select station, datehour, count(1) as incidents from stationincidents group by station, datehour")

print("we now have incidents by station/hour in incidentcount")
incidentcount.show(10)


# now join the two tables
joined = cleanedaverages.join(incidentcount, ['station', 'datehour'], 'outer')

# if incident data doesn't exist for that station/datehour, then it is 0
zeroed = joined.rdd.map(lambda row: Row(station = row.station, datehour=row.datehour, temp = row.temp, wind = row.wind, incidents = row.incidents if row.incidents  else 0)).toDF()

# if temp/wind data doesn't exist for that station/datehour, then we can't use that row
final = zeroed.filter(zeroed.temp.isNotNull()).filter(zeroed.wind.isNotNull()).filter(zeroed.temp!=0)

# finally apply correlation test
vecs = final.rdd.map(lambda row: Vectors.dense([row.temp,row.wind,row.incidents]))
print(Statistics.corr(vecs))
