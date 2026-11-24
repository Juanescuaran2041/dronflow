package com.dronflow.maintenance;

import com.dronflow.configuration.MaintenanceThresholds;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MaintenanceThresholdsTest {

    @Test
    void recommendsOnlyWhenAThresholdIsReached() {
        MaintenanceThresholds thresholds = new MaintenanceThresholds(100, 50);
        assertTrue(thresholds.exceededBy(101, 10));   // 95 h + 6 h
        assertFalse(thresholds.exceededBy(42, 10));   // 40 h + 2 h
        assertTrue(thresholds.exceededBy(10, 50));    // por número de misiones
    }
}
