package org.home.kafka_service.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Map;
import lombok.Data;

@Data
public class Message {

    @JsonProperty("business_id")
    private String businessId;
    @JsonProperty("name")
    private String name;
    @JsonProperty("address")
    private String address;
    @JsonProperty("city")
    private String city;
    @JsonProperty("state")
    private String state;
    @JsonProperty("postal_code")
    private String postalCode;
    @JsonProperty("latitude")
    private String latitude;
    @JsonProperty("longitude")
    private String longitude;
    @JsonProperty("stars")
    private String stars;
    @JsonProperty("review_count")
    private String reviewCount;
    @JsonProperty("is_open")
    private String isOpen;
    @JsonProperty("attributes")
    private Map<String, String> attributes;
    @JsonProperty("categories")
    private String categories;
    @JsonProperty("hours")
    private Map<String, String> hours;
}
