from app.db.models.interaction import Interaction
from app.db.neo4j_db import driver
from app.repository.generic_relationship_neo4j import create_relationship


def create_interaction(interaction):
    return create_relationship(
        start_entity="Device",
        start_identifier_key="id",
        start_identifier_value=interaction["from_device"],
        end_entity="Device",
        end_identifier_key="id",
        end_identifier_value=interaction["to_device"],
        relationship="CONNECTED",
        rel_properties=Interaction(**interaction).__dict__
    )




def is_device_busy(device_id, timestamp):
    query = """
    MATCH (a:Device {id: $device_id})-[r:CONNECTED]->()
    WHERE r.timestamp = $timestamp
    RETURN COUNT(r) > 0 AS is_busy
    """
    try:
        with driver.session() as session:
            result = session.run(query, {"device_id": device_id, "timestamp": timestamp}).single()
            return result["is_busy"] if result else False
    except Exception as e:
        return {"error": "Database Error", "details": str(e)}