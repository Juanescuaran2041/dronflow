package com.dronflow.user;

import org.junit.jupiter.api.Test;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.web.server.ResponseStatusException;

import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class UserServiceTest {

    private final UserRepository repository = mock(UserRepository.class);
    private final PasswordEncoder encoder = new BCryptPasswordEncoder();
    private final RevokedTokenRepository revokedTokens = mock(RevokedTokenRepository.class);
    private final UserService service = new UserService(repository, encoder, mock(JwtEncoder.class), revokedTokens);

    private User stored(User user) {
        when(repository.findById(user.getId())).thenReturn(Optional.of(user));
        when(repository.save(any(User.class))).thenAnswer(call -> call.getArgument(0));
        return user;
    }

    @Test
    void anOperatorIsPromotedToAdministrator() {
        User user = stored(new User("operador1", encoder.encode("contrasena1"), Role.OPERATOR));

        assertEquals(Role.ADMIN, service.promoteToAdmin(user.getId()).getRole());
        verify(repository).save(user);
    }

    @Test
    void anAdministratorCannotBePromotedAgain() {
        User user = stored(new User("admin", encoder.encode("contrasena1"), Role.ADMIN));

        assertEquals(409, assertThrows(ResponseStatusException.class, () -> service.promoteToAdmin(user.getId())).getStatusCode().value());
        verify(repository, never()).save(any(User.class));
    }

    @Test
    void aDeactivatedAccountCannotBePromoted() {
        User user = stored(new User("operador1", encoder.encode("contrasena1"), Role.OPERATOR));
        user.deactivate();

        assertEquals(409, assertThrows(ResponseStatusException.class, () -> service.promoteToAdmin(user.getId())).getStatusCode().value());
        assertEquals(Role.OPERATOR, user.getRole());
        verify(repository, never()).save(any(User.class));
    }

    @Test
    void promotingAnUnknownUserIsNotFound() {
        UUID id = UUID.randomUUID();
        when(repository.findById(id)).thenReturn(Optional.empty());

        assertEquals(404, assertThrows(ResponseStatusException.class, () -> service.promoteToAdmin(id)).getStatusCode().value());
    }
}
