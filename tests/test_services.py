import pytest
from datetime import datetime
from src.services import HotelManager
from src.exceptions import ResourceNotFoundError
from unittest.mock import patch

class TestHotelManager:
    @pytest.fixture
    def manager(self, tmp_path):
        hotels_file = tmp_path / "hotels.json"
        bookings_file = tmp_path / "bookings.json"

        hotels_file.write_text('''[
            {
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
                    {"roomType": "SGL", "roomId": "101"},
                    {"roomType": "SGL", "roomId": "102"}
                ]
            }
        ]''')

        bookings_file.write_text('''[
            {
                "hotelId": "H1",
                "arrival": "20240901",
                "departure": "20240903",
                "roomType": "SGL",
                "roomRate": "Standard"
            }
        ]''')

        return HotelManager(str(hotels_file), str(bookings_file))

    def test_load_hotels(self, manager):
        assert len(manager.hotels) == 1
        assert manager.hotels[0].id == "H1"
        assert len(manager.hotels[0].rooms) == 2

    def test_load_bookings(self, manager):
        assert len(manager.bookings) == 1
        assert manager.bookings[0].hotelId == "H1"
        assert manager.bookings[0].roomType == "SGL"

    def test_check_availability(self, manager):
        # Test single date availability
        assert manager.check_availability("H1", "20240901", "SGL") == 1
        assert manager.check_availability("H1", "20240904", "SGL") == 2

        # Test date range availability
        assert manager.check_availability(
            "H1", "20240901-20240902", "SGL") == 1

        # Test non-existent hotel
        with pytest.raises(ResourceNotFoundError):
            manager.check_availability("H2", "20240901", "SGL")

    # def test_search_availability(self, manager):
    #     with patch('datetime.datetime') as mock_date:
    #         mock_date.now.return_value = datetime(2024, 9, 1)
    #         result = manager.search_availability("H1", 5, "SGL")
    #         assert "(20241211-20241215, 2)" in result
