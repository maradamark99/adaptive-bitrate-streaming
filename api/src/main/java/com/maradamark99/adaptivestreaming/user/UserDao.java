package com.maradamark99.adaptivestreaming.user;

import java.util.Optional;

public interface UserDao {
    
    Optional<User> findByEmail(String email);

    boolean register(User user);

}
