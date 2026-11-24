package com.dronflow.mission;

import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Component;
import tools.jackson.core.type.TypeReference;
import tools.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.io.InputStream;
import java.io.UncheckedIOException;
import java.util.List;

// Las zonas vienen de restricted-zones.json, empaquetado en el backend
@Component
public class JsonRestrictedZoneProvider implements RestrictedZoneProvider {
    private final List<RestrictedZone> zones;

    public JsonRestrictedZoneProvider(ObjectMapper mapper) {
        try (InputStream in = new ClassPathResource("restricted-zones.json").getInputStream()) {
            this.zones = List.copyOf(mapper.readValue(in, new TypeReference<List<RestrictedZone>>() {}));
        } catch (IOException e) {
            throw new UncheckedIOException("Cannot read restricted-zones.json", e);
        }
    }

    @Override
    public List<RestrictedZone> getZones() {
        return zones;
    }
}
