import json
from datetime import datetime, timedelta
from typing import List, Tuple
from .models import Hotel, Booking
from .exceptions import ResourceNotFoundError

class HotelManager:
    def __init__(self, hotels_file: str, bookings_file: str):
        """
        Initialize HotelManager with data files.
        
        Args:
            hotels_file: Path to hotels JSON file
            bookings_file: Path to bookings JSON file
        """
        self.hotels = self._load_hotels(hotels_file)
        self.bookings = self._load_bookings(bookings_file)

    def _load_hotels(self, filename: str) -> List[Hotel]:
        with open(filename) as f:
            data = json.load(f)
            return [Hotel.from_dict(hotel) for hotel in data]

    def _load_bookings(self, filename: str) -> List[Booking]:
        with open(filename) as f:
            data = json.load(f)
            return [Booking.from_dict(booking) for booking in data]

    def _parse_date(self, date_str: str) -> datetime:
        return datetime.strptime(date_str, '%Y%m%d')

    def check_availability(self, hotel_id: str, date_str: str, room_type: str) -> int:
        """
        Check room availability for a given hotel, date and room type.
        
        Args:
            hotel_id: Hotel identifier
            date_str: Date or date range in YYYYMMDD format
            room_type: Room type code
            
        Returns:
            int: Number of available rooms
            
        Raises:
            ResourceNotFoundError: If hotel is not found
        """
        if '-' in date_str:
            start_date, end_date = map(self._parse_date, date_str.split('-'))
        else:
            start_date = self._parse_date(date_str)
            end_date = start_date + timedelta(days=1)

        hotel = next((h for h in self.hotels if h.id == hotel_id), None)
        if not hotel:
            raise ResourceNotFoundError(f"Hotel {hotel_id} not found")

        total_rooms = sum(1 for room in hotel.rooms if room.roomType == room_type)
        overlapping_bookings = sum(
            1 for booking in self.bookings
            if (booking.hotelId == hotel_id and
                booking.roomType == room_type and
                self._parse_date(booking.arrival) < end_date and
                self._parse_date(booking.departure) > start_date)
        )

        return max(0, total_rooms - overlapping_bookings)

    def search_availability(self, hotel_id: str, days: int, room_type: str) -> str:
        """
        Search for available rooms over a period.
        
        Args:
            hotel_id: Hotel identifier
            days: Number of days to search
            room_type: Room type code
            
        Returns:
            str: Formatted string showing availability periods
        """
        start_date = datetime.now()
        end_date = start_date + timedelta(days=days)
        available_periods = []
        current_period_start = None
        current_count = 0

        current_date = start_date
        while current_date < end_date:
            date_str = current_date.strftime('%Y%m%d')
            availability = self.check_availability(hotel_id, date_str, room_type)

            if availability > 0:
                if current_period_start is None:
                    current_period_start = current_date
                    current_count = availability
                elif availability != current_count:
                    if current_period_start:
                        available_periods.append(self._format_period(
                            current_period_start,
                            current_date - timedelta(days=1),
                            current_count
                        ))
                    current_period_start = current_date
                    current_count = availability
            else:
                if current_period_start is not None:
                    available_periods.append(self._format_period(
                        current_period_start,
                        current_date - timedelta(days=1),
                        current_count
                    ))
                    current_period_start = None

            current_date += timedelta(days=1)

        if current_period_start is not None:
            available_periods.append(self._format_period(
                current_period_start,
                current_date - timedelta(days=1),
                current_count
            ))

        return ', '.join(available_periods)

    def _format_period(self, start_date: datetime, end_date: datetime, count: int) -> str:
        """Format a single availability period."""
        start_str = start_date.strftime('%Y%m%d')
        end_str = end_date.strftime('%Y%m%d')
        if start_str == end_str:
            return f"({start_str}, {count})"
        return f"({start_str}-{end_str}, {count})" 