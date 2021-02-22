import os

from pyspark import SparkContext, SparkConf
from pyspark import SQLContext
from pyspark.sql.functions import col, from_json, lit
from pyspark.sql.types import StructType, StringType, IntegerType, \
    DecimalType, ByteType, MapType

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']


def get_schema():
    schema = StructType() \
        .add('business_id', StringType()) \
        .add('name', StringType()) \
        .add('address', StringType()) \
        .add('city', StringType()) \
        .add('state', StringType()) \
        .add('postal_code', IntegerType()) \
        .add('latitude', DecimalType(precision=10, scale=7)) \
        .add('longitude', DecimalType(precision=10, scale=7)) \
        .add('stars', DecimalType(precision=2, scale=1)) \
        .add('review_count', IntegerType()) \
        .add('is_open', ByteType()) \
        .add('attributes', MapType(keyType=StringType(), valueType=StringType())) \
        .add('categories', StringType()) \
        .add('hours', MapType(keyType=StringType(), valueType=StringType()))
    return schema


def anonymize(sql_context):

    schema = get_schema()

    df_raw = sql_context \
        .readStream \
        .format('kafka') \
        .option('kafka.bootstrap.servers', '127.0.0.1:9092') \
        .option('startingOffsets', 'earliest') \
        .option('subscribe', 'events') \
        .load()

    df_anmz = df_raw.select(from_json(col('value').cast('string'), schema).alias("parsed_value")) \
        .drop('name', 'address', 'latitude', 'longitude') \
        .withColumn('name', lit('REMOVED')) \
        .withColumn('address', lit('REMOVED')) \
        .withColumn('latitude', lit('REMOVED')) \
        .withColumn('longitude', lit('REMOVED'))

    return df_anmz


def write_to_s3(df):
    query = df.writeStream \
        .format('parquet') \
        .option('path', 's3a://kafka-task/output') \
        .option('checkpointLocation', 'checkpoint') \
        .start()
    query.awaitTermination()


if __name__ == "__main__":
    spark_conf = SparkConf() \
        .setMaster('local[*]') \
        .setAppName('anonymization_job')
    sc = SparkContext(conf=spark_conf)
    hadoopConf = sc._jsc.hadoopConfiguration()
    hadoopConf.set('fs.s3.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
    hadoopConf.set('fs.s3a.endpoint', 's3.us-east-1.amazonaws.com')
    hadoopConf.set('fs.s3a.awsAccessKeyId', AWS_ACCESS_KEY_ID)
    hadoopConf.set('fs.s3a.awsSecretAccessKey', AWS_SECRET_ACCESS_KEY)
    sql_context = SQLContext(sc)
    df = anonymize(sql_context)
    write_to_s3(df)
