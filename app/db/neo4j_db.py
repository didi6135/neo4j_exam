from neo4j import GraphDatabase

from app.settings.neo4j_config import NEO4J_URI, AUTH

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=AUTH
)