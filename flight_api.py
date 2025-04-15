import requests
import logging
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('flight_api.log')
    ]
)
logger = logging.getLogger(__name__)

class FlightAPI:
    def __init__(self):
        """Initialize the FlightAPI with the API key from environment variables."""
        load_dotenv()
        self.api_key = os.getenv('AVIATIONSTACK_API_KEY')
        if not self.api_key:
            logger.error("AVIATIONSTACK_API_KEY environment variable is not set")
            raise ValueError("AVIATIONSTACK_API_KEY environment variable is not set")
        self.base_url = "http://api.aviationstack.com/v1"
        self.cache = {}
        self.cache_timeout = timedelta(minutes=5)
        self.historical_data = defaultdict(list)  # Store historical data
        self.setup_logging()
        logger.info("FlightAPI initialized successfully")

    def setup_logging(self):
        self.logger = logging.getLogger(__name__)

    def _safe_get(self, data, *keys, default='Unknown'):
        """Safely get nested dictionary values."""
        try:
            for key in keys:
                if not isinstance(data, dict):
                    logger.debug(f"Expected dict, got {type(data)} for key {key}")
                    return default
                data = data.get(key)
                if data is None:
                    logger.debug(f"Key {key} not found in data")
                    return default
            return data
        except (AttributeError, TypeError) as e:
            logger.debug(f"Error accessing nested data: {str(e)}")
            return default

    def get_flight_info(self, flight_number):
        """Get current flight information."""
        try:
            logger.info(f"Processing request for flight {flight_number}")
            
            # Check cache first
            cache_key = f"{flight_number}_{datetime.now().strftime('%Y%m%d')}"
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if datetime.now() - timestamp < self.cache_timeout:
                    logger.info(f"Using cached data for flight {flight_number}")
                    return cached_data

            # Make API request
            params = {
                'access_key': self.api_key,
                'flight_iata': flight_number
            }
            
            logger.info(f"Making API request to {self.base_url}/flights")
            logger.debug(f"Request params: {params}")
            
            response = requests.get(f"{self.base_url}/flights", params=params)
            logger.debug(f"API Response status: {response.status_code}")
            
            response.raise_for_status()
            data = response.json()
            logger.debug(f"API Response data: {json.dumps(data, indent=2)}")

            if not data or 'data' not in data or not data['data']:
                logger.warning(f"No flight data found for {flight_number}")
                return {"error": "No flight data available"}

            flight_data = data['data'][0]

            # Extract flight information
            flight_info = {
                "flight_number": self._safe_get(flight_data, 'flight', 'iata'),
                "status": self._safe_get(flight_data, 'flight_status'),
                "departure_time": self._safe_get(flight_data, 'departure', 'scheduled'),
                "arrival_time": self._safe_get(flight_data, 'arrival', 'scheduled'),
                "gate": self._safe_get(flight_data, 'departure', 'gate'),
                "terminal": self._safe_get(flight_data, 'departure', 'terminal'),
                "aircraft": self._safe_get(flight_data, 'aircraft', 'iata'),
                "estimated_arrival": self._safe_get(flight_data, 'arrival', 'estimated'),
                "delay": self._safe_get(flight_data, 'departure', 'delay'),
                "codeshare": self._safe_get(flight_data, 'airline', 'name'),
                "codeshare_flight": self._safe_get(flight_data, 'flight', 'codeshared', 'flight_iata'),
                "destination": self._safe_get(flight_data, 'arrival', 'airport'),
                "departure_airport": self._safe_get(flight_data, 'departure', 'airport'),
                "departure_timezone": self._safe_get(flight_data, 'departure', 'timezone'),
                "arrival_timezone": self._safe_get(flight_data, 'arrival', 'timezone'),
                "ground_speed": self._safe_get(flight_data, 'live', 'speed_horizontal'),
                "altitude": self._safe_get(flight_data, 'live', 'altitude')
            }

            # Store historical data
            self._store_historical_data(flight_info)

            # Cache the result
            self.cache[cache_key] = (flight_info, datetime.now())
            logger.info(f"Successfully retrieved and cached flight info for {flight_number}")
            
            return flight_info

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return {"error": "Failed to fetch flight information"}
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {"error": "An unexpected error occurred"}

    def _store_historical_data(self, flight_info):
        """Store historical flight data."""
        try:
            flight_number = flight_info['flight_number']
            timestamp = datetime.now().isoformat()
            
            # Add timestamp to flight info
            historical_entry = {
                'timestamp': timestamp,
                **flight_info
            }
            
            # Store last 30 days of data
            self.historical_data[flight_number].append(historical_entry)
            self.historical_data[flight_number] = self.historical_data[flight_number][-30:]  # Keep last 30 entries
            
        except Exception as e:
            self.logger.error(f"Error storing historical data: {str(e)}")

    def get_historical_data(self, flight_number, days=7):
        """Get historical flight data for the specified number of days."""
        try:
            if flight_number not in self.historical_data:
                return {"error": "No historical data available"}
            
            cutoff_date = datetime.now() - timedelta(days=days)
            historical_flights = [
                flight for flight in self.historical_data[flight_number]
                if datetime.fromisoformat(flight['timestamp']) >= cutoff_date
            ]
            
            if not historical_flights:
                return {"error": f"No historical data available for the last {days} days"}
            
            # Calculate statistics
            delays = [int(flight['delay']) for flight in historical_flights if flight['delay'] != 'Unknown']
            avg_delay = sum(delays) / len(delays) if delays else 0
            
            on_time_count = sum(1 for flight in historical_flights if flight['delay'] == 'Unknown' or int(flight['delay']) <= 15)
            on_time_percentage = (on_time_count / len(historical_flights)) * 100
            
            return {
                "total_flights": len(historical_flights),
                "average_delay": round(avg_delay, 2),
                "on_time_percentage": round(on_time_percentage, 2),
                "flights": historical_flights
            }
            
        except Exception as e:
            self.logger.error(f"Error retrieving historical data: {str(e)}")
            return {"error": "Failed to retrieve historical data"}

    def get_all_flights(self) -> list:
        """Get a list of all available flights."""
        try:
            params = {
                'access_key': self.api_key,
                'limit': 100,
                'offset': 0
            }
            
            logger.info("Fetching all flights")
            response = requests.get(f"{self.base_url}/flights", params=params)
            
            if response.status_code != 200:
                logger.error(f"API request failed with status code {response.status_code}")
                return []
            
            data = response.json()
            if not data or not data.get('data'):
                logger.warning("No flight data available")
                return []
                
            return data['data']
            
        except Exception as e:
            logger.error(f"Error fetching all flights: {str(e)}")
            return []