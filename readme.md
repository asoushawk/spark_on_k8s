# Spark on K8S using Google's Spark Operator 

`This projects showcases PySpark on K8S`. You can run jobs in a K8S setup, having scalability and multi-workers pods and
automatic submition of spark jobs capabilities, all together with a S3A connection, being able to connect to S3 in order to do write and read operations.  

 ## You can run the job on Docker by using
 
  ### Build
     docker build --network=host -t {{image_name}} .
     
 ### Setup the envs and run
 
        docker run --net=host --mount type=bind,source="$(pwd)",target=/opt/application \
        -e AWS_KEY={{aws_key}} \
        -e AWS_SECRET={{aws_secret}} \
        -e FILE_PATH={{file_path}} \
        {{image_name}} \
        driver local:///opt/application/sample_pyspark_job.py

# Running on k8s

 #### 1 - Using the sample pyspark file write the Spark Job
 ```bash
  
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
      data.createOrReplaceTempView('data')
      
      df = spark.sql("SELECT * FROM data LIMIT 10")
      df.show()
 ```

    
 #### 2 - Containerize the Spark Job using the sample Dockerfile
  
     docker build --network=host -t {{image_name}} .
     
####  3 - Push the image to Docker Hub in order to later on, push into K8s
    
    docker push {{image_name}}
  
####  4 - Install Spark Operator, using the helm chart in `k8s/spark-operator_helm` you will have a `spark-operator` on, waiting for jobs to be submited
  ```bash
  $ helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator

  $ helm install my-release spark-operator/spark-operator --namespace spark-operator --create-namespace
  ```

     
  
####  5 - Submit jobs using `k8s/deploy_job/depĺoy_job.yaml`
  
      kubectl apply -f deploy_job.yaml
  ### deploy_job.yaml example
  ```bash
      apiVersion: "sparkoperator.k8s.io/v1beta2"
      kind: SparkApplication
      metadata:
        name: sparkjob
        namespace: default
      spec:
        type: Python
        mode: cluster
        image: asoushawk/pyspark-docker:dev
        imagePullPolicy: Always
        mainApplicationFile: "local:///app/sample_pyspark_job.py"
        sparkVersion: "3.0.0"
        driver:
          envVars:
            AWS_KEY: ""
            AWS_SECRET: ""
            FILE_PATH: ""
          cores: 1
          coreLimit: "1200m"
          memory: "512m"
          labels:
            version: 3.0.0
          serviceAccount: spark-spark


        executor:
          cores: 1
          instances: 2
          memory: "512m"
          labels:
            version: 3.0.0
 ```



  
 

