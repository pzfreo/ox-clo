

# ~/spark/bin/spark-submit --master local[*] wc.py "hdfs://localhost:54310/user/oxclo/books/*"

from pyspark import SparkContext, SparkConf
import sys

conf = SparkConf().setAppName("wordCount")
sc = SparkContext(conf=conf)


books = sc.textFile(sys.argv[1])
split = books.flatMap(lambda line: line.split())
stripped = split.map(lambda input: ''.join(filter(str.isalpha, input)))
numbered = stripped.map(lambda word: (word, 1))
wordcount = numbered.reduceByKey(lambda a,b: a+b)

for k,v in wordcount.collect():
  print (k,v)

sc.stop()
