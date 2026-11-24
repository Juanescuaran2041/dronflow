package com.dronflow.mission;

import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;

import java.util.List;

// Consulta con filtros opcionales; Spring Data la une a MissionRepository por el sufijo "Impl"
class MissionQueryRepositoryImpl implements MissionQueryRepository {
    private final MongoTemplate mongo;

    MissionQueryRepositoryImpl(MongoTemplate mongo) {
        this.mongo = mongo;
    }

    @Override
    public List<Mission> find(MissionFilter f) {
        Query q = new Query().with(Sort.by(Sort.Direction.DESC, "createdAt"));
        if (f.droneCode() != null) q.addCriteria(Criteria.where("assignedDroneCode").is(f.droneCode()));
        if (f.state() != null) q.addCriteria(Criteria.where("state").is(f.state()));
        if (f.from() != null || f.to() != null) {
            Criteria c = Criteria.where("createdAt");
            if (f.from() != null) c = c.gte(f.from());
            if (f.to() != null) c = c.lte(f.to());
            q.addCriteria(c);
        }
        return mongo.find(q, Mission.class);
    }
}
