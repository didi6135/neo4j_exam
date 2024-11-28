from app.db.models.device import Device
from app.repository.device_repository import create_device


def process_devices(devices):
    list(map(process_device, devices))

def process_device(device_data):
    location_data = device_data["location"]
    location = Device.Location(**location_data)
    device = Device(
        id=device_data["id"],
        brand=device_data["brand"],
        model=device_data["model"],
        os=device_data["os"],
        location=location,
    )
    create_device(device)
