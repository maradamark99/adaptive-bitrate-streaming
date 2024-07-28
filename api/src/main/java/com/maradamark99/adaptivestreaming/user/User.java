package com.maradamark99.adaptivestreaming.user;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

@AllArgsConstructor
@Data
@Builder
public class User {

    private Long id;
    
    private String email;

    private String username;

    private String password;
    
}
