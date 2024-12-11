from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class RoomType:
    code: str
    description: str
    amenities: List[str]
    features: List[str]

@dataclass
class Room:
    roomType: str
    roomId: str

@dataclass
class Hotel:
    id: str
    name: str
    roomTypes: List[RoomType]
    rooms: List[Room]

    @classmethod
    def from_dict(cls, data: Dict) -> 'Hotel':
        return cls(
            id=data['id'],
            name=data['name'],
            roomTypes=[
                RoomType(
                    code=rt['code'],
                    description=rt['description'],
                    amenities=rt.get('amenities', []),
                    features=rt.get('features', [])
                ) for rt in data['roomTypes']
            ],
            rooms=[Room(**room) for room in data['rooms']]
        )

@dataclass
class Booking:
    hotelId: str
    arrival: str
    departure: str
    roomType: str
    roomRate: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'Booking':
        return cls(**data) 