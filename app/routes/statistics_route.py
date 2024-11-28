from flask import Blueprint, jsonify

from app.repository.device_repository import find_bluetooth_connected_devices, find_devices_with_strong_signal, \
    count_connected_devices, check_direct_connection, fetch_most_recent_interaction

statistics_blueprint = Blueprint('statistics', __name__)


@statistics_blueprint.route("/connected_devices/bluetooth", methods=['GET'])
def get_bluetooth_connected_devices():
    try:
        data = find_bluetooth_connected_devices()
        if "error" in data:
            return jsonify({"error": data["error"], "details": data["details"]}), 500
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500



@statistics_blueprint.route("/connected_devices/strong_signal", methods=['GET'])
def get_devices_with_strong_signal():
    try:
        data = find_devices_with_strong_signal()
        if "error" in data:
            return jsonify({"error": data["error"], "details": data["details"]}), 500
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


@statistics_blueprint.route("/connected_devices/count/<string:device_id>", methods=['GET'])
def get_connected_device_count(device_id):
    try:
        data = count_connected_devices(device_id)
        if "error" in data:
            return jsonify({"error": data["error"], "details": data["details"]}), 500
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500



@statistics_blueprint.route("/connected_devices/direct/<string:device_id_1>/<string:device_id_2>", methods=['GET'])
def check_direct_connection_endpoint(device_id_1, device_id_2):
    try:
        data = check_direct_connection(device_id_1, device_id_2)
        if "error" in data:
            return jsonify({"error": data["error"], "details": data["details"]}), 500
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500



@statistics_blueprint.route("/connected_devices/most_recent/<string:device_id>", methods=['GET'])
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
