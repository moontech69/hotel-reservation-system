import pytest
from src.validators import validate_date_format, validate_hotel_id, validate_room_type
from src.models import Hotel, RoomType, Room
from src.exceptions import DateFormatError

@pytest.fixture
def sample_hotel():
    return Hotel(
        id="H1",
        name="Test Hotel",
        roomTypes=[
            RoomType(code="SGL", description="Single", amenities=[], features=[])
        ],
        rooms=[Room(roomType="SGL", roomId="101")]
    )

class TestValidators:
    def test_date_format_validation(self):
        assert validate_date_format("20240901") == True
        
        with pytest.raises(DateFormatError):
            validate_date_format("2024090")
        
        with pytest.raises(DateFormatError):
            validate_date_format("2024/09/01")
        
        with pytest.raises(DateFormatError):
            validate_date_format("20241301")  # Invalid month

    def test_hotel_id_validation(self, sample_hotel):
        assert validate_hotel_id("H1", [sample_hotel]) == True
        assert validate_hotel_id("H2", [sample_hotel]) == False

    def test_room_type_validation(self, sample_hotel):
        assert validate_room_type("SGL", "H1", [sample_hotel]) == True
        assert validate_room_type("DBL", "H1", [sample_hotel]) == False
        assert validate_room_type("SGL", "H2", [sample_hotel]) == False 