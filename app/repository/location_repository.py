from app.db.models.location import Location
from app.repository.generic_crud_neo4j import create


def create_location(location):
    return create('Location', location, Location)

