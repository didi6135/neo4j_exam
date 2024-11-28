from dataclasses import dataclass


@dataclass
class Device:
    class Location:
        latitude: float
        longitude: float
        altitude_meters: int
        accuracy_meters: int

    id: str
    brand: str
    model: str
    os: str
    location: Location