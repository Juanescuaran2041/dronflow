package com.dronflow.mission;

import com.dronflow.mission.dto.CreateMissionRequest;
import com.dronflow.mission.dto.MissionResponse;
import com.dronflow.mission.dto.RedirectRequest;
import jakarta.validation.Valid;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.util.List;

@RestController
@RequestMapping("/api/v1/missions")
public class MissionController {
    private final MissionService service;

    public MissionController(MissionService service) {
        this.service = service;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public MissionResponse create(@Valid @RequestBody CreateMissionRequest data) {
        return MissionResponse.of(service.create(data));
    }

    // HU-17: solo administrador (regla en SecurityConfig)
    @GetMapping
    public List<MissionResponse> find(@RequestParam(required = false) String droneCode,
                                      @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) Instant from,
                                      @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) Instant to,
                                      @RequestParam(required = false) MissionState state) {
        return service.find(new MissionFilter(droneCode, from, to, state)).stream().map(MissionResponse::of).toList();
    }

    @GetMapping("/{code}")
    public MissionResponse findByCode(@PathVariable String code) {
        return MissionResponse.of(service.findByCode(code));
    }

    @PostMapping("/{code}/authorize-takeoff")
    public MissionResponse authorizeTakeoff(@PathVariable String code) {
        return MissionResponse.of(service.authorizeTakeoff(code));
    }

    @PostMapping("/{code}/pause")
    public MissionResponse pause(@PathVariable String code) {
        return MissionResponse.of(service.pause(code));
    }

    @PostMapping("/{code}/resume")
    public MissionResponse resume(@PathVariable String code) {
        return MissionResponse.of(service.resume(code));
    }

    @PostMapping("/{code}/redirect")
    public MissionResponse redirect(@PathVariable String code, @Valid @RequestBody RedirectRequest request) {
        return MissionResponse.of(service.redirect(code, request.destination()));
    }

    @PostMapping("/{code}/abort")
    public MissionResponse abort(@PathVariable String code) {
        return MissionResponse.of(service.abort(code));
    }
}
