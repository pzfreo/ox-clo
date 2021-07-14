sudo pip3 install jupyter 
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS='notebook --no-browser'
pyspark --master spark://0.0.0.0:7077 \
     --packages  org.apache.hadoop:hadoop-aws:3.2.0

