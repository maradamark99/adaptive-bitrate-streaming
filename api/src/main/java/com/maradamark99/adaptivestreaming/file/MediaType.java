package com.maradamark99.adaptivestreaming.file;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

import java.util.Arrays;
import java.util.Set;
import java.util.stream.Collectors;

@Getter
@RequiredArgsConstructor
public enum MediaType {
    IMAGE(Set.of(".jpg", ".jpeg", ".gif", ".png", ".bmp")),
    VIDEO(Set.of(".mp4", ".avi", ".mov", ".wmv")),
    TEXT(Set.of(".txt", ".html", ".htm", ".xml", ".json"));

    private final Set<String> extensions;

    public static Set<MediaType> valueSet() {
        return Arrays.stream(MediaType.values()).collect(Collectors.toSet());
    }

    public String getMimeType() {
        return this.name().toLowerCase().concat("/");
    }

}
