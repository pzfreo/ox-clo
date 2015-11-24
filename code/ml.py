from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext


from dateutil.parser import parse
from datetime import datetime
from scipy import spatial
from numpy import array

from pyspark.mllib.clustering import KMeans, KMeansModel

conf = SparkConf().setAppName("wind-sfpd")
sc = SparkContext(conf=conf)
sqlc = SQLContext(sc)


df2 = sqlc.read.format('com.databricks.spark.csv').\
options(header='true', inferschema='true').\
load('/home/oxclo/datafiles/incidents/sfpd.csv.gz')

fixed = df2.rdd.map(lambda r: (parse(r.Date), [r.Y,r.X]))

only2014 = fixed.filter(lambda (d,l): d.year == 2014)

arrays = only2014.map(lambda (d,l): array(l))

clusters = KMeans.train(arrays, 5, maxIterations=10,
        runs=10, initializationMode="random")
        
        
for arr in clusters.centers:
	list = arr.tolist()
	print str(list[0]) +","+ str(list[1])
	
	
