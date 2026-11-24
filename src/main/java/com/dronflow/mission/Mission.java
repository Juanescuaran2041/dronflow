package com.dronflow.mission;

import com.dronflow.fleet.Location;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import java.time.Duration;
import java.time.Instant;
import java.util.UUID;

@Document("missions")
public class Mission {

    public static final int MAX_ROUTE_ATTEMPTS = 3;

    @Id
    private String code;
    private String type;
    private Priority priority;
    private Location origin;
    private Location destination;
    private double requiredPayload;
    private int minEndurance;
    private Route route;
    private String assignedDroneCode;
    private MissionState state;
    private int routeAttempts;
    private Instant createdAt;
    private Instant start;
    private Instant end;

    protected Mission() {}

    public Mission(String type, Priority priority, Location origin, Location destination,
                   double requiredPayload, int minEndurance) {
        if (origin.samePointAs(destination)) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Origin and destination must be different");
        }
        this.code = "M-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
        this.type = type;
        this.priority = priority;
        this.origin = origin;
        this.destination = destination;
        this.requiredPayload = requiredPayload;
        this.minEndurance = minEndurance;
        this.state = MissionState.PENDING;
        this.createdAt = Instant.now();
    }

    public void assignDrone(String droneCode) {
        requireState("assign a drone to", MissionState.PENDING);
        if (assignedDroneCode != null) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "The mission already has a drone");
        }
        this.assignedDroneCode = droneCode;
    }

    public void releaseDrone() {
        this.assignedDroneCode = null;
        this.routeAttempts = 0;
        this.route = null;
    }

    public int registerRouteAttempt() {
        return ++routeAttempts;
    }

    public void takeOff(Route validRoute) {
        requireState("take off", MissionState.PENDING);
        if (assignedDroneCode == null) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "The mission has no assigned drone yet");
        }
        this.route = validRoute;
        this.state = MissionState.TAKEOFF;
        this.start = Instant.now();
    }

    // Avance de la misión. Hoy lo reporta el operador; mañana, la telemetría del dron.
    public void reachCruise() {
        requireState("reach cruise altitude in", MissionState.TAKEOFF);
        state = MissionState.IN_PROGRESS;
    }

    public void startReturn() {
        requireState("start the return of", MissionState.IN_PROGRESS);
        state = MissionState.RETURNING;
    }

    public void finish() {
        requireState("finish", MissionState.RETURNING);
        state = MissionState.COMPLETED;
        end = Instant.now();
    }

    public void pause() {
        requireState("pause", MissionState.IN_PROGRESS);
        state = MissionState.PAUSED;
    }

    public void resume() {
        requireState("resume", MissionState.PAUSED);
        state = MissionState.IN_PROGRESS;
    }

    public void redirect(Location newDestination, Route newRoute) {
        requireState("redirect", MissionState.IN_PROGRESS);
        this.destination = newDestination;
        this.route = newRoute;
    }

    public void abort() {
        requireState("abort", MissionState.IN_PROGRESS, MissionState.PAUSED);
        state = MissionState.ABORTED;
        end = Instant.now();
    }

    public Duration flightDuration() {
        return start == null ? Duration.ZERO : Duration.between(start, end == null ? Instant.now() : end);
    }

    private void requireState(String action, MissionState... allowed) {
        for (MissionState s : allowed) {
            if (state == s) return;
        }
        throw new ResponseStatusException(HttpStatus.CONFLICT, "Cannot " + action + " the mission: it is " + state);
    }

    public String getCode() { return code; }
    public String getType() { return type; }
    public Priority getPriority() { return priority; }
    public Location getOrigin() { return origin; }
    public Location getDestination() { return destination; }
    public double getRequiredPayload() { return requiredPayload; }
    public int getMinEndurance() { return minEndurance; }
    public Route getRoute() { return route; }
    public String getAssignedDroneCode() { return assignedDroneCode; }
    public MissionState getState() { return state; }
    public int getRouteAttempts() { return routeAttempts; }
    public Instant getCreatedAt() { return createdAt; }
    public Instant getStart() { return start; }
    public Instant getEnd() { return end; }
}
