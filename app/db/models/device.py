from dataclasses import dataclass


@dataclass
class Device:
    @dataclass
    class Location:
        latitude: float
        longitude: float
        altitude_meters: int
        accuracy_meters: int

    id: str
    name: str
    brand: str
    model: str
    os: str
    location: Location