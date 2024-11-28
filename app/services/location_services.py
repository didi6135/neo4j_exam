from app.db.models.device import Device


def process_location(location_data):
    return Device.Location(
        latitude=location_data["latitude"],
        longitude=location_data["longitude"],
        altitude_meters=location_data["altitude_meters"],
        accuracy_meters=location_data["accuracy_meters"],
    )