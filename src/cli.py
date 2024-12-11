import argparse
import sys
from typing import Optional, List
from .services import HotelManager
from .validators import validate_date_format, validate_hotel_id, validate_room_type
from .exceptions import HotelReservationError, ValidationError, DateFormatError

class CLI:
    def __init__(self, manager: HotelManager):
        """
        Initialize CLI with a HotelManager instance.
        
        Args:
            manager: HotelManager instance to handle business logic
        """
        self.manager = manager

    def parse_command(self, command: str) -> Optional[dict]:
        """
        Parse input command and return command parameters.
        
        Args:
            command: Input command string
            
        Returns:
            dict: Command parameters or None if command is empty
            
        Raises:
            ValidationError: If command format is invalid
        """
        command = command.strip()
        if not command:
            return None

        if command.startswith('Availability('):
            if not command.endswith(')'):
                raise ValidationError("Invalid command format. Use: Availability(hotelId, date, roomType)")
            params = command[12:].strip('()').split(', ')
            if len(params) != 3:
                raise ValidationError("Invalid number of parameters. Expected: hotelId, date, roomType")
            return {
                'command': 'availability',
                'hotel_id': params[0],
                'date_str': params[1],
                'room_type': params[2]
            }

        elif command.startswith('Search('):
            if not command.endswith(')'):
                raise ValidationError("Invalid command format. Use: Search(hotelId, days, roomType)")
            params = command[7:].strip('()').split(', ')
            if len(params) != 3:
                raise ValidationError("Invalid number of parameters. Expected: hotelId, days, roomType")
            return {
                'command': 'search',
                'hotel_id': params[0],
                'days': params[1],
                'room_type': params[2]
            }
        else:
            raise ValidationError("Unknown command. Available commands: Availability(...), Search(...)")

    def validate_availability_params(self, params: dict) -> None:
        """Validate parameters for availability command."""
        if not validate_hotel_id(params['hotel_id'], self.manager.hotels):
            raise ValidationError(f"Hotel {params['hotel_id']} not found")

        if '-' in params['date_str']:
            start, end = params['date_str'].split('-')
            validate_date_format(start)
            validate_date_format(end)
        else:
            validate_date_format(params['date_str'])

        if not validate_room_type(params['room_type'], params['hotel_id'], self.manager.hotels):
            raise ValidationError(f"Room type {params['room_type']} not found in hotel {params['hotel_id']}")

    def validate_search_params(self, params: dict) -> None:
        """Validate parameters for search command."""
        if not validate_hotel_id(params['hotel_id'], self.manager.hotels):
            raise ValidationError(f"Hotel {params['hotel_id']} not found")

        try:
            days = int(params['days'])
            if days <= 0:
                raise ValidationError("Days must be a positive number")
        except ValueError:
            raise ValidationError("Days must be a valid number")

        if not validate_room_type(params['room_type'], params['hotel_id'], self.manager.hotels):
            raise ValidationError(f"Room type {params['room_type']} not found in hotel {params['hotel_id']}")

    def process_command(self, command: str) -> str:
        """
        Process a command and return the result.
        
        Args:
            command: Input command string
            
        Returns:
            str: Command result or error message
        """
        try:
            params = self.parse_command(command)
            if not params:
                return ""

            if params['command'] == 'availability':
                self.validate_availability_params(params)
                result = self.manager.check_availability(
                    params['hotel_id'],
                    params['date_str'],
                    params['room_type']
                )
                return str(result)

            elif params['command'] == 'search':
                self.validate_search_params(params)
                result = self.manager.search_availability(
                    params['hotel_id'],
                    int(params['days']),
                    params['room_type']
                )
                return result

        except HotelReservationError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(description='Hotel Reservation System')
    parser.add_argument('--hotels', required=True, help='Path to hotels JSON file')
    parser.add_argument('--bookings', required=True, help='Path to bookings JSON file')
    args = parser.parse_args()

    try:
        manager = HotelManager(args.hotels, args.bookings)
        cli = CLI(manager)

        while True:
            try:
                command = input("> ")
                if not command:
                    break
                result = cli.process_command(command)
                if result:
                    print(result)
            except EOFError:
                break

    except Exception as e:
        print(f"Fatal error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 