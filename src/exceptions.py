class HotelReservationError(Exception):
    """Base exception for hotel reservation system"""
    pass

class ValidationError(HotelReservationError):
    """Raised when validation fails"""
    pass

class ResourceNotFoundError(HotelReservationError):
    """Raised when a requested resource is not found"""
    pass

class DateFormatError(ValidationError):
    """Raised when date format is invalid"""
    pass 