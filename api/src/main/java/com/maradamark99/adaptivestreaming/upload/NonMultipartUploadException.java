package com.maradamark99.adaptivestreaming.upload;

public class NonMultipartUploadException extends RuntimeException {

    public NonMultipartUploadException() {
        super("Request must be multipart/form-data to upload files.");
    }
}
