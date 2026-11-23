package com.dronflow.fleet;

import com.dronflow.fleet.dto.RegisterDroneRequest;
import org.springframework.stereotype.Component;

@Component
public class InspectionDroneFactory implements DroneFactory {

    @Override
    public String type() {
        return "inspection";
    }

    @Override
    public Drone create(RegisterDroneRequest data) {
        return new InspectionDrone(data);
    }
}
