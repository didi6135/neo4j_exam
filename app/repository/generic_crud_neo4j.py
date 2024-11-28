import uuid
from dataclasses import fields

from app.db.neo4j_db import driver


def get_all(entity: str):
    with driver.session() as session:
        query = f"""
        match (e:{entity}) return e
        """
        try:
            res = session.run(query).data()
            return [dict(record['e']) for record in res] if res else None, {"error": "Get details Error", "details": "Getting details error"}
        except Exception as e:
            return None, {"error": "Database Error", "details": str(e)}


def get_one(entity:str, identifier_key: str, identifier_value: str):
    with driver.session() as session:
        query = f'''
        match (e:{entity} {{{identifier_key}: $identifier_value}}) return e
        '''
        params = {'name': identifier_value}
        try:
            res = session.run(query, params).single()
            return dict(res['e']) if res else None, {"error": "Get details Error", "details": "Getting details error"}
        except Exception as e:
            return None, {"error": "Database Error", "details": str(e)}


def create(entity:str, data:dict, model:type):
    with driver.session() as session:
        try:
            validated_data = model(**data)
        except TypeError as e:
            return None, {"error": "Validation Error", "details": str(e)}

        node_data = validated_data.__dict__

        query = f"""
        create (e:{entity} $data) return e
        """
        try:

            params = {'data': node_data}
            res = session.run(query, params).single()
            return dict(res['e']) if res else None, {"error": "Creation Error", "details": "Node creation failed"}

        except Exception as e:
            return None, {"error": "Database Error", "details": str(e)}



# def update(
#         entity:str,
#         identifier_key: str,
#         identifier_value: str,
#         update_details:dict,
#         model:type
# ):
#     with driver.session() as session:
#
#         model_fields = {f.name for f in fields(model)}
#
#         # Check for invalid fields
#         invalid_fields = set(update_details) - model_fields
#         if invalid_fields:
#             return None, {"error": "Validation Error", "details": f"Invalid fields: {', '.join(invalid_fields)}"}
#
#         query = f"""
#         match (e:{entity} {{{identifier_key}: $identifier_value}})
#         set e += $update_details
#         return e
#         """
#
#         params = {
#             'identifier_value': identifier_value,
#             'update_details': update_details
#         }
#         try:
#             res = session.run(query, params).single()
#             return dict(res['e']) if res else None, {"error": "Update Error", "details": "No node found or updated"}
#         except Exception as e:
#             return None, {"error": "Database Error", "details": str(e)}

def update(entity: str, identifier_key: str, identifier_value: str, data: dict):
    with driver.session() as session:
        query = f"""
        MATCH (e:{entity} {{{identifier_key}: $identifier_value}})
        SET e += $data
        RETURN e
        """
        params = {"identifier_value": identifier_value, "data": data}
        try:
            res = session.run(query, params).single()
            return dict(res['e']) if res else None
        except Exception as e:
            return {"error": "Database Error", "details": str(e)}



def delete(entity: str, identifier_key: str, identifier_value: str):
    with driver.session() as session:
        query = f"""
        MATCH (e:{entity} {{{identifier_key}: $identifier_value}})
        DETACH DELETE e
        RETURN COUNT(e) AS deleted_count
        """
        params = {
            "identifier_value": identifier_value
        }
        res = session.run(query, params).single()

        if res and res["deleted_count"] > 0:
            return True
        return False


