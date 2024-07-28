package com.maradamark99.adaptivestreaming.user;

public class UserAlreadyExistsWithEmailException extends RuntimeException {

    public UserAlreadyExistsWithEmailException(String message) {
        super(message);
    }
}
