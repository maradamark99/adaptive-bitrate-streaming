package com.maradamark99.adaptivestreaming.file;

import java.io.IOException;
import java.io.InputStream;

public interface FileTypeDetector {

    String detect(InputStream stream) throws IOException;

}
