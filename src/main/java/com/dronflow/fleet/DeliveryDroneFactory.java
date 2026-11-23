package com.dronflow.fleet;

import com.dronflow.fleet.dto.RegisterDroneRequest;
import org.springframework.stereotype.Component;

@Component
public class DeliveryDroneFactory implements DroneFactory {

    @Override
    public String type() {
        return "delivery";
    }

    @Override
    public Drone create(RegisterDroneRequest data) {
        return new DeliveryDrone(data);
    }
}
