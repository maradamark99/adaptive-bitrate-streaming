package com.maradamark99.adaptivestreaming.user;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.maradamark99.adaptivestreaming.auth.RegistrationRequest;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserDao userDao;

    private final PasswordEncoder passwordEncoder;
    
    public User getUserFromAuthentication(Authentication auth) {
        var userDetails = (UserDetails) auth.getPrincipal();
        return findByEmail(userDetails.getUsername());
    }

    public User findByEmail(String email) {
        return userDao
            .findByEmail(email)
            .orElseThrow(() -> new UsernameNotFoundException(email));
    }

    public void register(RegistrationRequest toRegister) {
        if (userDao.findByEmail(toRegister.email()).isPresent()) {
            throw new UserAlreadyExistsWithEmailException(toRegister.email());
        }

        var user = User
            .builder()
            .email(toRegister.email())
            .username(toRegister.username())
            .password(passwordEncoder.encode(toRegister.password()))
            .build();

        userDao.register(user);
    }

}
