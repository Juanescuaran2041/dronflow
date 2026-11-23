package com.dronflow.fleet.dto;

import com.dronflow.fleet.Drone;
import com.dronflow.fleet.DroneState;
import com.dronflow.fleet.Location;

import java.util.List;

public record DroneResponse(
        String code,
        String type,
        int batteryCapacity,
        double batteryLevelPercent,
        int enduranceMin,
        double maxPayload,
        List<String> equipment,
        Location location,
        DroneState state
) {
    public static DroneResponse of(Drone drone) {
        return new DroneResponse(drone.getCode(), drone.getType(), drone.getBatteryCapacity(),
                drone.getBatteryLevelPercent(), drone.getEnduranceMin(), drone.getMaxPayload(),
                drone.getEquipment(), drone.getLocation(), drone.getState());
    }
}
