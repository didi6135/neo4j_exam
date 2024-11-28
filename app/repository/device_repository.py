from dataclasses import asdict
from app.db.neo4j_db import driver



def create_device(device):
    with driver.session() as session:
        device_dict = asdict(device)

        query = """
        MERGE (d:Device {id: $id})
        ON CREATE SET
            d.name = $name,
            d.brand = $brand,
            d.model = $model,
            d.os = $os,
            d.latitude = $latitude,
            d.longitude = $longitude,
            d.altitude_meters = $altitude_meters,
            d.accuracy_meters = $accuracy_meters
        RETURN d
        """

        params = {
            "id": device_dict["id"],
            "name": device_dict["name"],
            "brand": device_dict["brand"],
            "model": device_dict["model"],
            "os": device_dict["os"],
            "latitude": device_dict["location"]["latitude"],
            "longitude": device_dict["location"]["longitude"],
            "altitude_meters": device_dict["location"]["altitude_meters"],
            "accuracy_meters": device_dict["location"]["accuracy_meters"],
        }
        res = session.run(query, params).single()
        return res if res else None



def find_bluetooth_connected_devices():
    query = """
    MATCH path = (a:Device)-[r:CONNECTED*]->(b:Device)
    WHERE ALL(rel IN relationships(path) WHERE rel.method = 'Bluetooth')
    RETURN [node IN nodes(path) | {id: node.id, name: node.name, brand: node.brand, model: node.model, os: node.os}] AS devices,
           length(path) AS path_length
    """
    try:
        with driver.session() as session:
            return [
                {"devices": record["devices"], "path_length": record["path_length"]}
                for record in session.run(query)
            ]
    except Exception as e:
        return {"error": "Database Error", "details": str(e)}



def find_devices_with_strong_signal():
    query = """
    MATCH path = (a:Device)-[r:CONNECTED*]->(b:Device)
    WHERE ALL(rel IN relationships(path) WHERE rel.signal_strength_dbm > -60)
    RETURN [node IN nodes(path) | {id: node.id, name: node.name, brand: node.brand, model: node.model, os: node.os}] AS devices,
           length(path) AS path_length
    """
    try:
        with driver.session() as session:
            return [
                {"devices": record["devices"], "path_length": record["path_length"]}
                for record in session.run(query)
            ]
    except Exception as e:
        return {"error": "Database Error", "details": str(e)}



def count_connected_devices(device_id):
    query = """
    MATCH (:Device {id: $device_id})-[:CONNECTED]->(connected:Device)
    RETURN COUNT(connected) AS count
    """
    try:
        with driver.session() as session:
            result = session.run(query, {"device_id": device_id}).single()
            return {"count": result["count"]} if result else {"count": 0}
    except Exception as e:
        return {"error": "Database Error", "details": str(e)}



def check_direct_connection(device_id_1, device_id_2):
    query = """
    MATCH (a:Device {id: $device_id_1})-[r:INTERACTED]->(b:Device {id: $device_id_2})
    RETURN COUNT(r) > 0 AS is_connected
    """
    try:
        with driver.session() as session:
            result = session.run(query, {"device_id_1": device_id_1, "device_id_2": device_id_2}).single()
            return {"is_connected": result["is_connected"]} if result else {"is_connected": False}
    except Exception as e:
        return {"error": "Database Error", "details": str(e)}



def fetch_most_recent_interaction(device_id):
    query = """
    MATCH (a:Device {id: $device_id})-[r:INTERACTED]->(b:Device)
    RETURN b.id AS connected_device_id, b.name AS connected_device_name, 
           r.method AS method, r.timestamp AS timestamp
    ORDER BY r.timestamp DESC
    LIMIT 1
    """
    try:
        with driver.session() as session:
            result = session.run(query, {"device_id": device_id}).single()
            return {
                "connected_device_id": result["connected_device_id"],
                "connected_device_name": result["connected_device_name"],
                "method": result["method"],
                "timestamp": result["timestamp"]
            } if result else None
    except Exception as e:
        return {"error": "Database Error", "details": str(e)}
