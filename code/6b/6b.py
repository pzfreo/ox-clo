from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row


conf = SparkConf().setAppName("clo2016")
sc = SparkContext(conf=conf)
sqlc = SQLContext(sc)

df = sqlc.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load("/home/oxclo/datafiles/practices/*.csv")

print df.rdd.count()

simpler = df.rdd.map(lambda x: (x.postcode.split()[0], 1))
nums = simpler.countByKey()

print "OX1", nums['OX1']
print "SW11", nums['SW11']