from app.db.models.interaction import Interaction
from app.repository.generic_relationship_neo4j import create_relationship


def create_interaction(interaction):
    create_relationship(
        start_entity="Device",
        start_identifier_key="id",
        start_identifier_value=interaction["from_device"],
        end_entity="Device",
        end_identifier_key="id",
        end_identifier_value=interaction["to_device"],
        relationship="CONNECTED",
        rel_properties=Interaction(**interaction).__dict__
    )