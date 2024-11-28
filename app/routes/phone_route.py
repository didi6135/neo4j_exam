from flask import Blueprint, request, jsonify

from app.repository.device_repository import find_bluetooth_connected_devices, find_devices_with_strong_signal, \
    count_connected_devices, check_direct_connection, fetch_most_recent_interaction
from app.services.data_serivces import process_data, process_record
from app.services.device_services import process_device

phone_blueprint = Blueprint('phone', __name__)

@phone_blueprint.route("/phone_tracker", methods=['POST'])
def get_interaction():
   try:
        data = request.json

        process_record(data)

        return jsonify({}), 200
   except Exception as e:
       print(str(e))
       return jsonify({}), 500


@phone_blueprint.route("/connected_devices/bluetooth", methods=['GET'])
def get_bluetooth_connected_devices():
    try:
        data = find_bluetooth_connected_devices()
        if "error" in data:
            return jsonify({"error": data["error"], "details": data["details"]}), 500
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


@phone_blueprint.route("/connected_devices/strong_signal", methods=['GET'])
def get_devices_with_strong_signal():
    try:
        data = find_devices_with_strong_signal()
        if "error" in data:
            return jsonify({"error": data["error"], "details": data["details"]}), 500
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


@phone_blueprint.route("/connected_devices/count/<string:device_id>", methods=['GET'])
def get_connected_device_count(device_id):
    try:
        data = count_connected_devices(device_id)
        if "error" in data:
            return jsonify({"error": data["error"], "details": data["details"]}), 500
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500



@phone_blueprint.route("/connected_devices/direct/<device_id_1>/<device_id_2>", methods=['GET'])
def check_direct_connection_endpoint(device_id_1, device_id_2):
    try:
        data = check_direct_connection(device_id_1, device_id_2)
        if "error" in data:
            return jsonify({"error": data["error"], "details": data["details"]}), 500
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500



@phone_blueprint.route("/connected_devices/most_recent/<device_id>", methods=['GET'])
def get_most_recent_interaction(device_id):
    try:
        data = fetch_most_recent_interaction(device_id)
        if "error" in data:
            return jsonify({"error": data["error"], "details": data["details"]}), 500
        if not data:
            return jsonify({"message": "No interactions found for the given device"}), 404
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
