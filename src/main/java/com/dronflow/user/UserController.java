package com.dronflow.user;

import com.dronflow.user.dto.LoginRequest;
import com.dronflow.user.dto.RegisterOperatorRequest;
import com.dronflow.user.dto.Session;
import com.dronflow.user.dto.UserResponse;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1")
public class UserController {
    private final UserService service;

    public UserController(UserService service) {
        this.service = service;
    }

    @PostMapping("/auth/login")
    public Session login(@Valid @RequestBody LoginRequest loginRequest) {
        return service.login(loginRequest.userName(), loginRequest.password());
    }

    @PostMapping("/users")
    @ResponseStatus(HttpStatus.CREATED)
    public UserResponse registerOperator(@Valid @RequestBody RegisterOperatorRequest request) {
        return UserResponse.of(service.registerOperator(request.userName(), request.password()));
    }

    @PostMapping("/logout")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void logout(@AuthenticationPrincipal Jwt jwt) {
        service.logout(jwt.getId(), jwt.getExpiresAt());
    }
}
