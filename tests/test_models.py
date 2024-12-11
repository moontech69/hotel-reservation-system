import pytest
from src.models import Hotel, RoomType, Room, Booking

class TestModels:
    def test_room_type_creation(self):
        room_type = RoomType(
            code="SGL",
            description="Single Room",
            amenities=["WiFi"],
            features=["Non-smoking"]
        )
        assert room_type.code == "SGL"
        assert "WiFi" in room_type.amenities

    def test_room_creation(self):
        room = Room(roomType="SGL", roomId="101")
        assert room.roomType == "SGL"
        assert room.roomId == "101"

    def test_hotel_from_dict(self):
        hotel_data = {
            "id": "H1",
            "name": "Test Hotel",
            "roomTypes": [
                {
                    "code": "SGL",
                    "description": "Single Room",
                    "amenities": ["WiFi"],
                    "features": ["Non-smoking"]
                }
            ],
            "rooms": [
                {"roomType": "SGL", "roomId": "101"}
            ]
        }
        
        hotel = Hotel.from_dict(hotel_data)
        assert hotel.id == "H1"
        assert len(hotel.roomTypes) == 1
        assert hotel.roomTypes[0].code == "SGL"
        assert len(hotel.rooms) == 1
        assert hotel.rooms[0].roomId == "101"

    def test_booking_from_dict(self):
        booking_data = {
            "hotelId": "H1",
            "arrival": "20240901",
            "departure": "20240903",
            "roomType": "SGL",
            "roomRate": "Standard"
        }
        
        booking = Booking.from_dict(booking_data)
        assert booking.hotelId == "H1"
        assert booking.arrival == "20240901"
        assert booking.departure == "20240903" 