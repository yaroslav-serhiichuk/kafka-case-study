FROM adoptopenjdk/openjdk11
WORKDIR /usr/kafka-producer-service
COPY target/kafka-producer-service-0.0.1-SNAPSHOT.jar .
ENTRYPOINT ["java", "-cp", "/usr/kafka-producer-service/kafka-producer-service-0.0.1-SNAPSHOT.jar", \
            "-Dloader.main=org.home.kafka_service.KafkaProducerApplication", "org.springframework.boot.loader.PropertiesLauncher"]
