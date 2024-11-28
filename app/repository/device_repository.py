from app.db.models.device import Device
from app.repository.generic_crud_neo4j import create, get_all, get_one, update, delete


def create_device(device):
    return create('Device', device, Device)
#
#
# def get_all_devices():
#     return get_all("Device")
#
#
# def get_device_by_id(device_id):
#     return get_one("Device", "id_device", device_id)
#
#
# def update_device(device_id, updates):
#     return update("Device", "id_device", device_id, updates)
#
#
# def delete_device(device_id):
#     return delete("Device", "id_device", device_id)

