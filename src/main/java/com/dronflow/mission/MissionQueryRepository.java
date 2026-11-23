package com.dronflow.mission;

import java.util.List;

public interface MissionQueryRepository {
    List<Mission> find(MissionFilter filter);
}
