import pyspark
from pyspark.sql import SQLContext,SparkSession
from pyspark.sql.types import StringType, IntegerType, StructField, StructType, DoubleType, LongType
from pyspark.sql.functions import *
from google.cloud import storage

spark = SparkSession.builder.master("yarn")\
.appName("Test")\
.config("spark.sql.broadcastTimeout", "36000")\
.config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")\
.getOrCreate()

def count_files(bucket):
  blobs = storage.Client().list_blobs(bucket)
  count = 0
  for blob in blobs:
    if "rawdata/nyc-yellow-taxi/yellow_tripdata_2020" in blob.name:
        count += 1
  return count

dataSchema = StructType([
  StructField("VendorID", IntegerType()),
  StructField("tpep_pickup_datetime", StringType()),
  StructField("tpep_dropoff_datetime", StringType()),
  StructField("passenger_count", IntegerType()),
  StructField("trip_distance", DoubleType()),
  StructField("RatecodeID", IntegerType()),
  StructField("store_and_fwd_flag", StringType()),
  StructField("PULocationID", IntegerType()),
  StructField("DOLocationID", IntegerType()),
  StructField("payment_type", IntegerType()),
  StructField("fare_amount", DoubleType()),
  StructField("extra", DoubleType()),
  StructField("mta_tax", DoubleType()),
  StructField("tip_amount", DoubleType()),
  StructField("tolls_amount", DoubleType()),
  StructField("improvement_surcharge", DoubleType()),
  StructField("total_amount", DoubleType()),
  StructField("congestion_surcharge", DoubleType()),
])

df = (spark.read
      .format("csv")
      .option("delimiter", ",")
      .option("header", True)
      .schema(dataSchema)
      .load("gs://tsi-ucf-data/rawdata/nyc-yellow-taxi/yellow_tripdata_2020-*.csv")
)

cleaned_df = (df.withColumn("Year", year(col("tpep_pickup_datetime")))
              .withColumn("Month", month(col("tpep_pickup_datetime")))
              .filter((col("Year") == "2020") & ((col("Month") <= count_files("tsi-ucf-data"))))
)

rides_per_day = (cleaned_df.withColumn("Day", dayofmonth("tpep_pickup_datetime"))
                 .groupBy(col("Day"),col("Month"))
                 .agg(count("tpep_pickup_datetime").alias("Rides"))
                 .sort(col("Day"))
                )
				
(rides_per_day
 .coalesce(1)
 .write
 .format("bigquery")
 .option("temporaryGcsBucket", "dataproc-staging-europe-west3-1007106565013-gtgvut0n")
 .option("table", "test_data.test_table_v2")
 .partitionBy("Month")
 .mode("overwrite")
 .save()
)
