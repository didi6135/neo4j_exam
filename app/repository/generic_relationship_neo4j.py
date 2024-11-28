from app.db.neo4j_db import driver


def create_relationship(
        start_entity: str,
        start_identifier_key: str,
        start_identifier_value: str,
        end_entity: str,
        end_identifier_key: str,
        end_identifier_value: str,
        relationship: str,
        start_properties: dict = None,
        end_properties: dict = None,
        rel_properties: dict = None
):
    with driver.session() as session:
        query = f"""
        MERGE (a:{start_entity} {{{start_identifier_key}: $start_identifier_value}})
        ON CREATE SET a += $start_properties
        MERGE (b:{end_entity} {{{end_identifier_key}: $end_identifier_value}})
        ON CREATE SET b += $end_properties
        MERGE (a)-[r:{relationship}]->(b)
        SET r += $rel_properties
        RETURN type(r) AS relationship, properties(r) AS rel_properties
        """
        params = {
            'start_identifier_value': start_identifier_value,
            'end_identifier_value': end_identifier_value,
            'start_properties': start_properties or {},
            'end_properties': end_properties or {},
            'rel_properties': rel_properties or {}
        }

        try:
            res = session.run(query, params).single()
            return {
                'relationship': res['relationship'],
                'rel_properties': res['rel_properties']
            } if res else None
        except Exception as e:
            print(f"Error creating relationship: {str(e)}")
            return {"error": "Database Error", "details": str(e)}



