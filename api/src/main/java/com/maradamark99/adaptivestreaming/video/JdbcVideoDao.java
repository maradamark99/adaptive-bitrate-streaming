package com.maradamark99.adaptivestreaming.video;

import lombok.RequiredArgsConstructor;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
import org.springframework.stereotype.Repository;

import java.util.HashMap;

@Repository
@RequiredArgsConstructor
public class JdbcVideoDao implements VideoDao {

    private final JdbcTemplate jdbcTemplate;

    @Override
    public long save(VideoRequest video) {
        final var table = "videos";
        final var params = new HashMap<String, Object>();
        params.put("_key", video.getKey());
        params.put("bucket", video.getBucket());
        params.put("uploaded_by", video.getUploadedBy());
        var simpleInsert = new SimpleJdbcInsert(jdbcTemplate)
                .withTableName(table)
                .usingGeneratedKeyColumns("id");
        return simpleInsert.executeAndReturnKey(params).longValue();
    }

}
