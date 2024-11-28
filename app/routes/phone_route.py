from flask import Blueprint, request, jsonify

# from app.repository.device_repository import process_devices
from app.repository.interaction_repository import process_interaction
from app.services.data_serivces import process_data

phone_blueprint = Blueprint('phone', __name__)

@phone_blueprint.route("/phone_tracker", methods=['POST'])
def get_interaction():
   try:
        data = request.json

        process_data(data)

        # process_devices(devices)
        # process_interaction(interaction)

        return jsonify({}), 200
   except Exception as e:
       print(str(e))
       return jsonify({}), 500