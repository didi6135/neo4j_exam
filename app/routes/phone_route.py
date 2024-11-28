from flask import Blueprint, request, jsonify


from app.services.data_serivces import process_record

phone_blueprint = Blueprint('phone', __name__)

@phone_blueprint.route("/phone_tracker", methods=['POST'])
def get_interaction():
    try:
        data = request.json
        process_record(data)
        return jsonify({"message": "Interaction processed successfully"}), 200
    except Exception as e:
        error_message = str(e)
        print(f"Error processing interaction: {error_message}")
        return jsonify({"error": "Internal Server Error", "details": error_message}), 500



