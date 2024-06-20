package com.maradamark99.adaptivestreaming.file;

import lombok.RequiredArgsConstructor;

import org.apache.tika.Tika;

import java.io.IOException;
import java.io.InputStream;

@RequiredArgsConstructor
public class TikaFileTypeDetector implements FileTypeDetector {

	private final Tika tika;

	@Override
  public String detect(InputStream stream) throws IOException {
    return tika.detect(stream);
  }

}
