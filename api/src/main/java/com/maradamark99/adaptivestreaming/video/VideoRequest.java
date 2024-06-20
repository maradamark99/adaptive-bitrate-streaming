package com.maradamark99.adaptivestreaming.video;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class VideoRequest {
    private String bucket;
    private String key;
    private long uploadedBy;
}
