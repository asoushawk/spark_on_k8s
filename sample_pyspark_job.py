import os
from pyspark.sql import SparkSession

if __name__ == "__main__":
    

    aws_key        = os.environ['AWS_KEY']
    aws_secret_key = os.environ['AWS_SECRET']

    spark = SparkSession.builder \
                .appName("pyspark_job") \
                .getOrCreate()

    spark._jsc.hadoopConfiguration().set("fs.s3a.awsAccessKeyId",     aws_key)
    spark._jsc.hadoopConfiguration().set("fs.s3a.awsSecretAccessKey", aws_secret_key)
    spark._jsc.hadoopConfiguration().set("fs.s3a.impl","org.apache.hadoop.fs.s3a.S3AFileSystem")
    spark._jsc.hadoopConfiguration().set("fs.s3a.impl","org.apache.hadoop.fs.s3native.NativeS3FileSystem")
    spark._jsc.hadoopConfiguration().set("com.amazonaws.services.s3.enableV4", "true")
    spark._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider","org.apache.hadoop.fs.s3a.BasicAWSCredentialsProvider")
    spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "us-east-1.amazonaws.com")
    

    #simple sample job

    data = spark.read.json(os.environ['FILE_PATH'])
    data.createOrReplaceTempView("data")
    
    df = spark.sql("SELECT * FROM data LIMIT 10")
    df.show()




    