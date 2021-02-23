FROM ubuntu:18.04

ARG user=spark
ARG group=spark
ARG uid=1000
ARG gid=1000

ENV JAVA_HOME /usr/jdk-11.0.6+10
ENV SPARK_HOME /usr/spark-3.0.2-bin-hadoop3.2
ENV HADOOP_HOME /usr/hadoop-3.2.2

RUN apt-get update && \
  apt-get install -y apt-utils wget software-properties-common && \
  add-apt-repository ppa:deadsnakes/ppa && \
  apt-get update && \
  apt-get install -y python3.8 && \
  wget https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.6%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.6_10.tar.gz -P /usr && \
  wget https://apache.paket.ua/spark/spark-3.0.2/spark-3.0.2-bin-hadoop3.2.tgz -P /usr && \
  wget https://apache.paket.ua/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz -P /usr && \
  mkdir -p ${JAVA_HOME} && \
  mkdir -p ${SPARK_HOME} && \
  mkdir -p ${HADOOP_HOME} && \
  tar -xvzf /usr/OpenJDK11U-jdk_x64_linux_hotspot_11.0.6_10.tar.gz --directory /usr && \
  tar -xvzf /usr/spark-3.0.2-bin-hadoop3.2.tgz --directory /usr && \
  tar -xvzf /usr/hadoop-3.2.2.tar.gz --directory /usr && \
  rm /usr/OpenJDK11U-jdk_x64_linux_hotspot_11.0.6_10.tar.gz && \
  rm /usr/spark-3.0.2-bin-hadoop3.2.tgz && \
  rm /usr/hadoop-3.2.2.tar.gz && \
  export PATH=${PATH}:${JAVA_HOME}/bin:${SPARK_HOME}/bin && \
  ln -s /usr/bin/python3 /usr/bin/python && \
  apt-get install -y python3-pip && \
  ln -s /usr/bin/pip3 /usr/bin/pip && \
  pip install pyspark==3.0.2

WORKDIR /usr/spark-anonymizer
COPY anonymization_job.py .
ENTRYPOINT ["/usr/spark-3.0.2-bin-hadoop3.2/bin/spark-submit", \
            "--conf", "spark.jars.ivy=/tmp/.ivy", \
            "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.2,com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.3", \
            "anonymization_job.py"]
