package com.dronflow.user;

import com.dronflow.user.dto.Session;
import org.springframework.http.HttpStatus;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.oauth2.jose.jws.MacAlgorithm;
import org.springframework.security.oauth2.jwt.JwsHeader;
import org.springframework.security.oauth2.jwt.JwtClaimsSet;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.JwtEncoderParameters;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.UUID;

@Service
public class UserService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtEncoder jwtEncoder;
    private final RevokedTokenRepository revokedTokenRepository;

    public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder, JwtEncoder jwtEncoder, RevokedTokenRepository revokedTokenRepository) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtEncoder = jwtEncoder;
        this.revokedTokenRepository = revokedTokenRepository;
    }

    public Session login(String username, String password) {
        User user = userRepository.findByUsername(username).filter(u -> u.authenticate(password,  passwordEncoder)).orElseThrow(() -> new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid credentials"));
        Instant now = Instant.now();
        Role role = user.getRole();

        UUID id = UUID.randomUUID();

        JwtClaimsSet claims = JwtClaimsSet.builder()
                .id(id.toString())
                .subject(user.getUsername())
                .claim("role", role.name())
                .issuedAt(now).expiresAt(now.plus(2 , ChronoUnit.HOURS))
                .build();
        String token = jwtEncoder.encode(JwtEncoderParameters.from(JwsHeader.with(MacAlgorithm.HS256).build(), claims)).getTokenValue();
        return new Session(token, role);
    }

    public User registerOperator(String username, String password) {
        if (userRepository.findByUsername(username).isPresent()) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Username already exists");
        }
        return userRepository.save(new User(username, passwordEncoder.encode(password), Role.OPERATOR));
    }

    public User edit(UUID id, String username, String password) {
        User user = findById(id);
        if (username != null && !username.equals(user.getUsername())
                && userRepository.findByUsername(username).isPresent()) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Username already exists");
        }
        user.editData(username, password, passwordEncoder);
        return userRepository.save(user);
    }

    // Se da de baja, no se borra, para no perder el rastro de quién operó cada misión
    public void delete(UUID id) {
        User user = findById(id);
        // Ninguna cuenta de administrador se da de baja, ni la propia ni la de otro
        if (user.getRole() == Role.ADMIN) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Administrator accounts cannot be deleted");
        }
        user.deactivate();
        userRepository.save(user);
    }

    private User findById(UUID id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found"));
    }

    public void logout(String token, Instant expiresAt) {
        revokedTokenRepository.save(new RevokedTokens(token, expiresAt));
    }

}
