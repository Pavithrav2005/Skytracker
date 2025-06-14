import os
import requests
from dotenv import load_dotenv

load_dotenv()

AVIATIONSTACK_API_KEY = os.getenv('AVIATIONSTACK_API_KEY')
AVIATIONSTACK_API_URL = "http://api.aviationstack.com/v1/flights"

def qa_agent_respond(user_query: str) -> str:
    """Respond to user queries related to airline information."""
    if "status of flight" in user_query.lower():
        flight_number = extract_flight_number(user_query)
        if flight_number:
            return get_flight_status(flight_number)
        else:
            return '{"answer": "Please provide a valid flight number."}'
    else:
        return '{"answer": "I can only provide flight status information."}'

def extract_flight_number(query: str) -> str:
    """Extract flight number from the user query."""
    words = query.split()
    for word in words:
        if word.isalnum() and len(word) > 2:  # Simple check for flight number format
            return word
    return ""

def get_flight_status(flight_number: str) -> str:
    """Fetch flight status from the AviationStack API."""
    params = {
        'access_key': AVIATIONSTACK_API_KEY,
        'flight_iata': flight_number
    }
    response = requests.get(AVIATIONSTACK_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['data']:
            flight_info = data['data'][0]
            return f'Flight {flight_info["flight"]["iata"]} is currently {flight_info["status"]}.'
        else:
            return '{"answer": "No information found for the provided flight number."}'
    else:
        return '{"answer": "Error fetching data from the AviationStack API."}'