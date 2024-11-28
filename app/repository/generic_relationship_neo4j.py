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
            merge (a:{start_entity} {{{start_identifier_key}: $start_identifier_value}})
            on create set += $start_properties
            merge (b:{end_entity} {{{end_identifier_key}: $end_identifier_value}})
            on create set += $end_properties
            create (a)-[r:$relationship]->(b)
            return type(r) AS relationship, properties(r) AS rel_properties
            """

        params = {
            'start_identifier_value': start_identifier_value,
            'end_identifier_value': end_identifier_value,
            'relationship': relationship,
            'start_properties': start_properties or {},
            'end_properties': end_properties or {},
            'rel_properties': rel_properties
        }

        res = session.run(query, params).single()
        return {
            'relationship': res['relationship'],
            'rel_properties': res['rel_properties']
        } if res else None




def get_relationship_outgoing(
        entity:str,
        identifier_key:str,
        identifier_value:str,
        relationship:str
):
    with driver.session() as session:
        query = f"""
        match (a:{entity} {{{identifier_key}: $value}})-[r:{relationship}]->(b)
        RETURN type(r) AS relationship, properties(r) AS rel_properties, properties(b) AS end_node
        """
        params = {
            'value': identifier_value,
        }

        res = session.run(query, params).data()
        return [
            {
                'relationship': record['relationship'],
                'res_properties': record['rel_properties'],
                'end_node': record['end_node']
            }
            for record in res
        ]



def get_relationship_incoming(
        entity:str,
        identifier_key: str,
        identifier_value: str,
        relationship: str
):
    with driver.session() as session:
        query = f"""
        match (a:{entity} {{{identifier_key}: $value}})<-[r:{relationship}]-(b)
        RETURN type(r) AS relationship, properties(r) AS rel_properties, properties(b) AS end_node
        """
        params = {
            'value': identifier_value,
        }

        res = session.run(query, params).data()
        return [
            {
                'relationship': record['relationship'],
                'res_properties': record['rel_properties'],
                'end_node': record['end_node']
            }
            for record in res
        ]



def get_relationship_both(
        entity:str,
        identifier_key: str,
        identifier_value: str,
        relationship: str
):
    with driver.session() as session:
        query = f"""
        match (a:{entity} {{{identifier_key}: $value}})-[r:{relationship}]-(b)
        RETURN type(r) AS relationship, properties(r) AS rel_properties, properties(b) AS end_node
        """
        params = {
            'value': identifier_value,
        }

        res = session.run(query, params).data()
        return [
            {
                'relationship': record['relationship'],
                'res_properties': record['rel_properties'],
                'end_node': record['end_node']
            }
            for record in res
        ]



def delete_relationship(
        start_entity: str,
        start_identifier_key: str,
        start_identifier_value: str,
        end_entity: str,
        end_identifier_key: str,
        end_identifier_value: str,
        relationship: str
):
    with driver.session() as session:
        query = f"""
        match (a:{start_entity} {{{start_identifier_key}: $start_value}})
              -[r:{relationship}]->
              (b:{end_entity} {{{end_identifier_key}: $end_value}})
        delete r
        return COUNT(r) AS deleted_count
        """
        params = {
            "start_value": start_identifier_value,
            "end_value": end_identifier_value
        }
        res = session.run(query, params).single()
        return res["deleted_count"] > 0 if res else False