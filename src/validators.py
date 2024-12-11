from datetime import datetime
from typing import List
from .models import Hotel
from .exceptions import ValidationError, DateFormatError

def validate_date_format(date_str: str) -> bool:
    """
    Validate if a date string is in YYYYMMDD format.
    
    Args:
        date_str: String to validate
        
    Returns:
        bool: True if valid, False otherwise
        
    Raises:
        DateFormatError: If date format is invalid
    """
    if not date_str.isdigit() or len(date_str) != 8:
        raise DateFormatError("Date must be in YYYYMMDD format")
    try:
        datetime.strptime(date_str, '%Y%m%d')
        return True
    except ValueError as e:
        raise DateFormatError(f"Invalid date: {str(e)}")

def validate_hotel_id(hotel_id: str, hotels: List[Hotel]) -> bool:
    """
    Validate if hotel_id exists.
    
    Args:
        hotel_id: Hotel ID to validate
        hotels: List of available hotels
        
    Returns:
        bool: True if valid, False otherwise
    """
    return any(h.id == hotel_id for h in hotels)

def validate_room_type(room_type: str, hotel_id: str, hotels: List[Hotel]) -> bool:
    """
    Validate if room_type exists in the specified hotel.
    
    Args:
        room_type: Room type code to validate
        hotel_id: Hotel ID where to look for room type
        hotels: List of available hotels
        
    Returns:
        bool: True if valid, False otherwise
    """
    hotel = next((h for h in hotels if h.id == hotel_id), None)
    if not hotel:
        return False
    return any(rt.code == room_type for rt in hotel.roomTypes) 