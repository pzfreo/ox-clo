wget http://archive.cloudera.com/beta/livy/livy-server-0.3.0.zip
unzip livy-server-0.3.0.zip
cd livy-server-0.3.0
mkdir logs
echo "livy.spark.master = spark://0.0.0.0:7077" >> conf/livy.conf
bin/livy-server
