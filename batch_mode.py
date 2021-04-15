#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType

def purchase_sword_event_schema():
    """
    root
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User-Agent: string (nullable = true)
    |-- event_type: string (nullable = true)
    """
    return StructType([
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User-Agent", StringType(), True),
        StructField("event_type", StringType(), True),
    ])

# purchase_sword
@udf('boolean')
def is_purchase(event_as_json):
    event = json.loads(event_as_json)
    if event['event_type'] == 'purchase_sword':
        return True
    return False

def main():
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .enableHiveSupport() \
        .getOrCreate()

#     batch - load raw events
    raw_events = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "events") \
        .option("startingOffsets", "earliest") \
        .option("endingOffsets", "latest") \
        .load()

#     # streaming - load raw events
#     raw_events = spark \
#         .readStream \
#         .format("kafka") \
#         .option("kafka.bootstrap.servers", "kafka:29092") \
#         .option("subscribe", "events") \
#         .load()

    # filter for purchase_sword events
    purchase_events = raw_events \
        .filter(is_purchase(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          purchase_sword_event_schema()).alias('json')) \
        .select('raw_event', 'timestamp', 'json.*')

    # register extracted_purchase_events to temp table
    purchase_events.registerTempTable("sword_purchase_events")

    # write to parquet file
    spark.sql("""
        create external table sword_purchase_events
        stored as parquet
        location '/tmp/sword_purchase_events'
        as
        select * from sword_purchase_events
    """)

    sword_purchase_events.write.mode('overwrite').parquet('/tmp/sword_purchase_events')

#     # streaming
#     spark.sql("drop table if exists purchase_events")
#     sql_string = """
#         create external table if not exists purchase_events (
#             raw_event string,
#             timestamp string,
#             Accept string,
#             Host string,
#             `User-Agent` string,
#             event_type string
#             )
#             stored as parquet
#             location '/tmp/purchase_events'
#             tblproperties ("parquet.compress"="SNAPPY")
#             """
#     spark.sql(sql_string)
    
#     sink = purchase_events \
#         .writeStream \
#         .format("parquet") \
#         .option("checkpointLocation", "/tmp/checkpoints_for_sword_purchases") \
#         .option("path", "/tmp/purchase_events") \
#         .trigger(processingTime="10 seconds") \
#         .start()

#     sink.awaitTermination()

if __name__ == "__main__":
    main()

