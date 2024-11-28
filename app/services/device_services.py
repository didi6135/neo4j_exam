from app.db.models.device import Device
from app.repository.device_repository import create_device
from app.services.location_services import process_location


def process_devices(devices):
    list(map(process_device, devices))


def process_device(device_data):
    device = Device(
        id=device_data["id"],
        name=device_data['name'],
        brand=device_data["brand"],
        model=device_data["model"],
        os=device_data["os"],
        location=process_location(device_data["location"]),
    )
    return create_device(device)




