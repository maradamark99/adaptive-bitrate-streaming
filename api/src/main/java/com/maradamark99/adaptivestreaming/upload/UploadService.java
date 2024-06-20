package com.maradamark99.adaptivestreaming.upload;

import com.maradamark99.blobstorage.StorageClient;
import com.maradamark99.blobstorage.exception.FileUploadException;
import com.maradamark99.adaptivestreaming.file.FileConstraints;
import com.maradamark99.adaptivestreaming.file.FileTypeDetector;
import com.maradamark99.adaptivestreaming.file.MediaType;
import com.maradamark99.adaptivestreaming.video.VideoRequest;
import com.maradamark99.adaptivestreaming.video.VideoDao;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.apache.commons.fileupload2.jakarta.JakartaServletFileUpload;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class UploadService {

    private final Buckets buckets;

    private final FileConstraints fileConstraints;

    private final FileTypeDetector fileTypeDetector;

    private final StorageClient storageClient;

    private final VideoDao videoDao;

    @Transactional
    public void upload(HttpServletRequest request) throws IOException {
        var upload = new JakartaServletFileUpload<>();
        upload.setFileSizeMax(fileConstraints.getMaxSizeInBytes());
        var isMultipart = JakartaServletFileUpload.isMultipartContent(request);

        if (!isMultipart) {
            throw new NonMultipartUploadException();
        }

        upload.getItemIterator(request).forEachRemaining(item -> {
            var stream = item.getInputStream();
            String mimeType = fileTypeDetector.detect(stream);
            var mimeTypeParts = mimeType.split("/");

            if (!MediaType.VIDEO.getMimeType().startsWith(mimeTypeParts[0])) {
                throw new FileUploadException("You may only upload video files.");
            }

            var key = "%s.%s".formatted(UUID.randomUUID().toString(), mimeTypeParts[1]);
            var bucket = buckets.getVideos();
            storageClient.putObject(bucket, key, stream);
            videoDao.save(new VideoRequest(bucket, key, 1));
        });
    }

}







