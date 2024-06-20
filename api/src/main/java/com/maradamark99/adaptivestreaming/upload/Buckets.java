package com.maradamark99.adaptivestreaming.upload;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "blob-storage.buckets")
@Getter @Setter
public class Buckets {

    private String videos;

    private String thumbnails;

}
