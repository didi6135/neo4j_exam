from app.services.device_services import process_devices
from app.services.interaction_services import process_interaction


def process_data(data):
    return list(map(process_record, data))


def process_record(record):
    devices = record["devices"]
    device_results = process_devices(devices)

    interaction = record["interaction"]
    interaction_result = process_interaction(interaction)

    return {
        "devices": device_results,
        "interaction": interaction_result
    }
