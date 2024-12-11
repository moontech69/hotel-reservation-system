import pytest
from datetime import datetime
from src.cli import CLI
from src.services import HotelManager
from src.exceptions import ValidationError
from unittest.mock import patch

@pytest.fixture
def cli(tmp_path):
    # Create test files
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

    manager = HotelManager(str(hotels_file), str(bookings_file))
    return CLI(manager)


class TestCLI:
    def test_parse_availability_command(self, cli):
        result = cli.parse_command("Availability(H1, 20240901, SGL)")
        assert result == {
            'command': 'availability',
            'hotel_id': 'H1',
            'date_str': '20240901',
            'room_type': 'SGL'
        }

    def test_parse_search_command(self, cli):
        result = cli.parse_command("Search(H1, 5, SGL)")
        assert result == {
            'command': 'search',
            'hotel_id': 'H1',
            'days': '5',
            'room_type': 'SGL'
        }

    def test_invalid_command_format(self, cli):
        with pytest.raises(ValidationError):
            cli.parse_command("Availability(H1, 20240901)")
        with pytest.raises(ValidationError):
            cli.parse_command("Search(H1, 5)")

    def test_process_availability_command(self, cli):
        result = cli.process_command("Availability(H1, 20240901, SGL)")
        assert result == "1"  # One room available

    # def test_process_search_command(self, cli):
    #     with patch('datetime.datetime') as mock_date:
    #         mock_date.now.return_value = datetime(2024, 9, 1)
    #         result = cli.process_command("Search(H1, 5, SGL)")
    #         assert "(20241211-20241215, 2)" in result

    def test_error_handling(self, cli):
        result = cli.process_command("Availability(H2, 20240901, SGL)")
        assert "Error: Hotel H2 not found" in result

        result = cli.process_command("Availability(H1, 2024/09/01, SGL)")
        assert "Error: Date must be in YYYYMMDD format" in result

        result = cli.process_command("Search(H1, -1, SGL)")
        assert "Error: Days must be a positive number" in result
