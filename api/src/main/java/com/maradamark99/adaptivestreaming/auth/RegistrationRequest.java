package com.maradamark99.adaptivestreaming.auth;

import org.hibernate.validator.constraints.Length;

import com.maradamark99.adaptivestreaming.security.PasswordConfig;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Pattern;

public record RegistrationRequest(
    @Length(min = 4, max = 255) 
    String username, 
    
    @Email 
    String email, 
    
    @Pattern(regexp = PasswordConfig.STRONG_PASSWORD_PATTERN) 
    String password) {
    
}
