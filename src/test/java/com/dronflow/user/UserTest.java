package com.dronflow.user;

import org.junit.jupiter.api.Test;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class UserTest {

    private final PasswordEncoder encoder = new BCryptPasswordEncoder();

    private User newOperator() {
        return new User("operador1", encoder.encode("contrasena1"), Role.OPERATOR);
    }

    @Test
    void editChangesUserNameAndPassword() {                 // RF-23
        User user = newOperator();
        user.editData("operador2", "contrasena2", encoder);
        assertEquals("operador2", user.getUsername());
        assertTrue(user.authenticate("contrasena2", encoder));
        assertFalse(user.authenticate("contrasena1", encoder));
    }

    @Test
    void editKeepsWhatIsNotSent() {                         // RF-23
        User user = newOperator();
        user.editData(null, "contrasena2", encoder);
        assertEquals("operador1", user.getUsername());

        user.editData("operador3", "   ", encoder);
        assertEquals("operador3", user.getUsername());
        assertTrue(user.authenticate("contrasena2", encoder));
    }

    @Test
    void aDeactivatedUserCannotAuthenticate() {             // RF-22
        User user = newOperator();
        user.deactivate();
        assertFalse(user.isActive());
        assertFalse(user.authenticate("contrasena1", encoder));
    }
}
