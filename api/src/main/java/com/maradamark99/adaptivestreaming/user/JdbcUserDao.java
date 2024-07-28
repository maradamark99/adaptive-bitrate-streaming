package com.maradamark99.adaptivestreaming.user;

import java.util.Optional;

import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Component;

import lombok.RequiredArgsConstructor;

@Component
@RequiredArgsConstructor
public class JdbcUserDao implements UserDao {

    private final JdbcTemplate template;

    @Override
    public Optional<User> findByEmail(String email) {
        final var sql = "SELECT id, email, username, password FROM users WHERE email = ?";

        RowMapper<User> mapper = (rs, rowNum) -> {
            return new User(
                rs.getLong("id"),
                rs.getString("email"),
                rs.getString("username"),
                rs.getString("password") 
            );
        };
        try {
            return Optional.of(template.queryForObject(sql, mapper, email));
        } catch (EmptyResultDataAccessException e) {
            return Optional.empty();
        }
        
    }

    @Override
    public boolean register(User user) {
        final var sql = "INSERT INTO users (email, username, password) VALUES (?, ?, ?)";
        return template.update(sql, user.getEmail(), user.getUsername(), user.getPassword()) > 0;
    }
    
}
