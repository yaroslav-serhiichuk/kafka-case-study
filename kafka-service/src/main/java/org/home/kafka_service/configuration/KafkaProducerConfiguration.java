package org.home.kafka_service.configuration;

import java.util.Map;

import org.apache.kafka.common.serialization.StringSerializer;
import org.home.kafka_service.entity.Message;

import io.confluent.kafka.serializers.KafkaJsonSerializer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;

@Configuration
@PropertySource("/application.properties")
public class KafkaProducerConfiguration {

    @Value("${producer.events.topic}")
    private  String eventsTopic;

    @Bean
    public ProducerFactory<String, Message> producerFactory(KafkaProperties kafkaProperties) {
        Map<String, Object> configProperties = kafkaProperties.buildProducerProperties();
        configProperties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        configProperties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, KafkaJsonSerializer.class);
        return new DefaultKafkaProducerFactory<>(configProperties);
    }

    @Bean
    public KafkaTemplate<String, Message> eventsKafkaTemplate(KafkaProperties kafkaProperties) {
        var kafkaTemplate = new KafkaTemplate<>(producerFactory(kafkaProperties));
        kafkaTemplate.setDefaultTopic(eventsTopic);
        return kafkaTemplate;
    }
}
