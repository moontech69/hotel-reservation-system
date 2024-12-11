# Hotel Reservation System

The **Hotel Reservation System** is a command-line application designed to manage hotel room availability and bookings. This tool enables users to query room availability and search for open slots over a specified date range.

## Features

- **Check Room Availability:** Verify how many rooms of a specific type are available on a given date or date range.
- **Search Availability:** Find available rooms for a hotel within a future time window.
- **Support for Multiple Room Types:** Handles various room types with specific features and amenities.
- **Data-Driven:** Reads hotel and booking data from JSON files.
- **Robust Testing:** Includes a comprehensive unit test suite for reliability.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/moontech69/hotel-reservation-system.git
   cd hotel-reservation-system
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

---

## Usage

Run the application with the required JSON data files:

```bash
myapp --hotels data/hotels.json --bookings data/bookings.json
```

### Commands

1. **Check Availability**

   ```bash
   Availability(hotelId, date, roomType)
   ```

   Example:

   ```bash
   Availability(H1, 20240901, SGL)
   ```

2. **Search Availability**
   ```bash
   Search(hotelId, days, roomType)
   ```
   Example:
   ```bash
   Search(H1, 5, DBL)
   ```

---

## Development

### Setup

1. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -e .
   ```

### Running Tests

To ensure all functionalities are working as expected, run the test suite:

```bash
pytest
```

---

## Project Structure

```plaintext
hotel-reservation-system/
├── data/                     # Sample data files
│   ├── hotels.json
│   ├── bookings.json
├── src/                      # Source code
│   ├── cli.py                # Command-line interface
│   ├── exceptions.py         # Custom exceptions
│   ├── models.py             # Data models for Hotel, Room, etc.
│   ├── services.py           # Core business logic
│   ├── validators.py         # Input validation logic
├── tests/                    # Test suite
│   ├── test_cli.py           # Tests for the CLI
│   ├── test_models.py        # Tests for data models
│   ├── test_services.py      # Tests for business logic
│   ├── test_validators.py    # Tests for validation logic
├── README.md                 # Project documentation
├── requirements.txt          # Project dependencies
├── setup.py                  # Project setup file
├── venv/                     # Virtual environment
```

---

## Sample Data Files

### `hotels.json`

```json
[
	{
		"id": "H1",
		"name": "Hotel California",
		"roomTypes": [
			{
				"code": "SGL",
				"description": "Single Room",
				"amenities": ["WiFi", "TV"],
				"features": ["Non-smoking"]
			},
			{
				"code": "DBL",
				"description": "Double Room",
				"amenities": ["WiFi", "TV", "Minibar"],
				"features": ["Non-smoking", "Sea View"]
			}
		],
		"rooms": [
			{ "roomType": "SGL", "roomId": "101" },
			{ "roomType": "SGL", "roomId": "102" },
			{ "roomType": "DBL", "roomId": "201" },
			{ "roomType": "DBL", "roomId": "202" }
		]
	}
]
```

### `bookings.json`

```json
[
	{
		"hotelId": "H1",
		"arrival": "20240901",
		"departure": "20240903",
		"roomType": "DBL",
		"roomRate": "Prepaid"
	},
	{
		"hotelId": "H1",
		"arrival": "20240902",
		"departure": "20240905",
		"roomType": "SGL",
		"roomRate": "Standard"
	}
]
```
