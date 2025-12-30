from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from clickhouse_connect import get_client

spark = SparkSession.builder.appName("KafkaToClickHouse").getOrCreate()

schema = StructType([
    StructField("timestamp", TimestampType(), True),
    StructField("level", StringType(), True),
    StructField("service", StringType(), True),
    StructField("message", StringType(), True),
    StructField("trace_id", StringType(), True),
    StructField("tenant_id", StringType(), True)
])

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "redpanda:9092") \
    .option("subscribe", "raw_logs") \
    .option("startingOffsets", "earliest") \
    .load()

df_parsed = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

client = get_client(host='clickhouse', port=8123, username='default', password='')

def write_to_clickhouse(batch_df, batch_id):
    if not batch_df.rdd.isEmpty():
        data = [tuple(row) for row in batch_df.collect()]
        client.insert('logs.raw_logs', data)

df_parsed.writeStream \
    .foreachBatch(write_to_clickhouse) \
    .outputMode("append") \
    .start() \
    .awaitTermination()
