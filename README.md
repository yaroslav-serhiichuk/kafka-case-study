# Kafka case-study
This is simple streaming pipeline which consumes JSON data object consume this
data, anonymize it and write in parquet format to Amazon S3. All components are run in Docker containers.

## Prerequisites
To run this pipeline following tools required:
- Docker
- docker-compose
- Amazon S3 bucket created and its name exported to environment variable
- AWS credentials are exported to environment variables 

## Services
Please use diagram.jpg to find following services: 

### 1. Kafka producer service
This is Spring Boot application which consumes POST requests on /event endpoint and pushes json objects to "events" topic.
Spring kafka connector used for this purpose.

### 2. Kafka broker
This is single broker, built using wurstmeister-kafka image. It has only one topic - "events" with single partition.

### 3. Spark anonymizer
This is pyspark structured streaming job which reads json objects from "events" topic as streaming dataframes, replaces sensitive data to "REMOVED" statement, saves result to parquet files and pushes them to Amazon S3.

## Pipeline run
Before deploying pipeline please make sure that AWS credentials (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY) are present in environment variables, and you AWS account has permission to write to S3.
Also, you need to export AWS_BUCKET environment variable with name of your S3 bucket (as s3 bucket names must be unique across AWS accounts).
To deploy all components you need just run deploy.sh script.

After finishing deployment process you can send POST requests using tool loki Postman to http://localhost:8080/event and attach to the request body json object with following schema:

~~~
{
    "business_id": string,
    "name": string,
    "address": string,
    "city": string,
    "state": string,
    "postal_code": integer,
    "latitude": decimal(10,7),
    "longitude": decimal(10,7),
    "stars": decimal(2,1),
    "review_count": integer,
    "is_open": byte,
    "attributes": {
        attribute: string
    },
    "categories": string,
    "hours": {
        day: string
    }
}
~~~

Anonymized parqut files in real time will be landed in your S3 bucket "output" directory.