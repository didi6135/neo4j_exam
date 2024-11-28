from app.services.device_services import process_devices
from app.services.interaction_services import process_interaction


def process_data(data):
    list(map(process_record, data))


def process_record(record):
    process_devices(record["devices"])
    process_interaction(record["interaction"])