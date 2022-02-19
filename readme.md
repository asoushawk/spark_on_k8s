# Spark on K8S using Google's Spark Operator 

This projects lets you deploy pyspark jobs in a k8s setup, having scalability and multi-workers and
automatic submition of spark jobs capabilities, all together with a S3A connection, being able to connect to S3 in order to do write and read operations.  

Running

    1 - Using the sample file, write the spark job.
    2 - Containerize the spark job using the sample Dockerfile
    3 - Push the image to Docker Hub in order to later on, push into K8s
    4 - Install spark-operator, using helm chart in `k8s/spark-operator_helm`
        - Now, you will have a spark-operator on, waiting for jobs to be submited
    5 - Submit jobs using `k8s/deploy_job/depĺoy_job.yaml`
        