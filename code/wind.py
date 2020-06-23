from pyspark.sql import SQLContext, Row
from pyspark.sql.functions import max, mean, col
sqlc = SQLContext(sc)
df = sqlc.read.csv('/home/oxclo/datafiles/wind/2015/*',header='true',inferSchema='true')

df.createOrReplaceTempView('wind')
sqlContext.sql("SELECT Station_ID, avg(Wind_Velocity_Mtr_Sec) as avg,max(Wind_Velocity_Mtr_Sec) as max from wind group by Station_ID").show()

df.groupBy('Station_ID').agg(mean(col('Wind_Velocity_Mtr_Sec')), max(col('Wind_Velocity_Mtr_Sec'))).show()

cleanDF = df.rdd.map(lambda row: \
	Row(station = row.Station_ID, \
    wind = row.Wind_Velocity_Mtr_Sec)).toDF()
cleanDF.show()
