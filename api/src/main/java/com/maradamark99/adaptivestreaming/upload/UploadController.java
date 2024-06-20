package com.maradamark99.adaptivestreaming.upload;

import com.maradamark99.blobstorage.exception.FileUploadException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import jakarta.servlet.http.HttpServletRequest;
import java.io.IOException;

@Slf4j
@RestController
@RequestMapping("/api/v1/upload")
@RequiredArgsConstructor
public class UploadController {

    private final UploadService uploadService;

    @PostMapping
    public ResponseEntity<?> upload(HttpServletRequest request) throws IOException, FileUploadException {
        uploadService.upload(request);
        return ResponseEntity.accepted().build();
    }

}
