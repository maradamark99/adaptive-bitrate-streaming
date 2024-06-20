package com.maradamark99.adaptivestreaming.file;

import lombok.Getter;
import lombok.Setter;

import java.util.HashSet;
import java.util.Set;

@Getter
public class FileConstraints {

    @Setter
    private Set<MediaType> allowedMediaTypes;

    private Set<String> allowedFileExtensions;

    private long maxSizeInBytes;

    private long minSizeInBytes;

    public FileConstraints(Set<MediaType> allowedMediaTypes, Set<String> allowedFileExtensions, long maxSizeInBytes, long minSizeInBytes) {
        setAllowedMediaTypes(allowedMediaTypes);
        setAllowedFileExtensions(allowedFileExtensions);
        setMinSizeInBytes(minSizeInBytes);
        setMaxSizeInBytes(maxSizeInBytes);
    }

    public FileConstraints() {
    }

    public void setAllowedFileExtensions(Set<String> fileExtensions) {
        if (allowedMediaTypes != null) {
            var set = new HashSet<String>();
            for (var aFileType : allowedMediaTypes) {
                for (var aFileExtension : fileExtensions) {
                    if (aFileType.getExtensions().contains(aFileExtension)) {
                        set.add(aFileExtension);
                    }
                }
            }
            this.allowedFileExtensions = set;
        } else {
            this.allowedFileExtensions = fileExtensions;
        }
    }

    public void setMaxSizeInBytes(long maxSizeInBytes) {
        if (maxSizeInBytes < 0 || maxSizeInBytes < minSizeInBytes) {
            throw new IllegalArgumentException();
        }
        this.maxSizeInBytes = maxSizeInBytes;
    }

    public void setMinSizeInBytes(long minSizeInBytes) {
        if (minSizeInBytes < 0 || minSizeInBytes > maxSizeInBytes) {
            throw new IllegalArgumentException();
        }
        this.minSizeInBytes = minSizeInBytes;
    }

    public static FileConstraintsBuilder builder() {
        return new FileConstraintsBuilder();
    }

    public static final class FileConstraintsBuilder {

        private Set<MediaType> allowedFileTypes;

        private Set<String> allowedFileExtensions;

        private long maxSizeInBytes;

        private long minSizeInBytes;

        public FileConstraintsBuilder withAllowedFileTypes(Set<MediaType> fileTypes) {
            this.allowedFileTypes = fileTypes;
            return this;
        }

        public FileConstraintsBuilder withAllowedFileExtensions(Set<String> fileExtensions) {
            this.allowedFileExtensions = fileExtensions;
            return this;
        }

        public FileConstraintsBuilder withMinSizeInBytes(long minSize) {
            this.minSizeInBytes = minSize;
            return this;
        }

        public FileConstraintsBuilder withMaxSizeInBytes(long maxSize) {
            this.maxSizeInBytes = maxSize;
            return this;
        }

        public FileConstraints build() {
            var constraints = new FileConstraints();
            constraints.setAllowedFileExtensions(allowedFileExtensions);
            constraints.setAllowedMediaTypes(allowedFileTypes);
            constraints.setMinSizeInBytes(minSizeInBytes);
            constraints.setMaxSizeInBytes(maxSizeInBytes);
            return constraints;
        }

    }

}