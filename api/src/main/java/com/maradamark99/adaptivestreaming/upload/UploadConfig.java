package com.maradamark99.adaptivestreaming.upload;

import com.maradamark99.adaptivestreaming.file.FileConstraints;
import com.maradamark99.adaptivestreaming.file.FileTypeDetector;
import com.maradamark99.adaptivestreaming.file.MediaType;
import com.maradamark99.adaptivestreaming.file.TikaFileTypeDetector;
import org.apache.tika.Tika;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.Set;

@Configuration
public class UploadConfig {

    private static final long MAX_SIZE_IN_BYTES = (long) (Math.pow(1024, 3) * 10);

    @Bean
    FileConstraints fileConstraints() {
        return FileConstraints.builder()
                .withAllowedFileTypes(Set.of(MediaType.VIDEO))
                .withMaxSizeInBytes(MAX_SIZE_IN_BYTES)
                .build();
    }

    @Bean
    FileTypeDetector fileTypeDetector() {
        return new TikaFileTypeDetector(new Tika());
    }

}
