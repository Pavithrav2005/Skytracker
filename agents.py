# agents.py
import json
import re
from flight_api import FlightAPI

# Initialize the FlightAPI
flight_api = FlightAPI()

# Define airline codes with their full names
AIRLINE_CODES = {
    # Major International Airlines
    'BA': 'British Airways',
    'AA': 'American Airlines',
    'DL': 'Delta Air Lines',
    'UA': 'United Airlines',
    
    # Other Major Airlines
    'LH': 'Lufthansa',
    'AF': 'Air France',
    'KL': 'KLM',
    'EK': 'Emirates',
    'SQ': 'Singapore Airlines',
    'QF': 'Qantas',
    'CX': 'Cathay Pacific',
    'JL': 'Japan Airlines',
    'NH': 'ANA',
    'QR': 'Qatar Airways',
    'EY': 'Etihad Airways',
    'TK': 'Turkish Airlines',
    'CA': 'Air China',
    'MU': 'China Eastern',
    'CZ': 'China Southern',
    
    # Regional Airlines
    'VS': 'Virgin Atlantic',
    'IB': 'Iberia',
    'AZ': 'ITA Airways',
    'SK': 'SAS',
    'FI': 'Icelandair',
    'AY': 'Finnair',
    'OS': 'Austrian Airlines',
    'LX': 'Swiss International Air Lines',
    'SN': 'Brussels Airlines',
    'TP': 'TAP Portugal',
    'LO': 'LOT Polish Airlines',
    'SU': 'Aeroflot',
    'AC': 'Air Canada',
    'NZ': 'Air New Zealand',
    'SA': 'South African Airways',
    'ET': 'Ethiopian Airlines',
    'MS': 'EgyptAir',
    'SV': 'Saudia',
    'AI': 'Air India',
    'TG': 'Thai Airways',
    'GA': 'Garuda Indonesia',
    'MH': 'Malaysia Airlines',
    'PR': 'Philippine Airlines',
    'KE': 'Korean Air',
    'OZ': 'Asiana Airlines',
    'BR': 'EVA Air',
    'CI': 'China Airlines',
    
    # Additional Regional and National Airlines
    'OM': 'MIAT Mongolian Airlines',
    'KC': 'Air Astana',
    'HY': 'Uzbekistan Airways',
    'B2': 'Belavia',
    'PS': 'Ukraine International Airlines',
    'RO': 'TAROM',
    'JU': 'Air Serbia',
    'FB': 'Bulgaria Air',
    'BT': 'Air Baltic',
    'A3': 'Aegean Airlines',
    'ME': 'Middle East Airlines',
    'RJ': 'Royal Jordanian',
    'KU': 'Kuwait Airways',
    'WY': 'Oman Air',
    'PK': 'Pakistan International Airlines',
    'UL': 'SriLankan Airlines',
    'VN': 'Vietnam Airlines',
    'BI': 'Royal Brunei Airlines',
    'MF': 'Xiamen Airlines',
    'FM': 'Shanghai Airlines',
    'HU': 'Hainan Airlines',
    '3U': 'Sichuan Airlines',
    
    # Additional Airlines
    'AM': 'Aeromexico',
    'AR': 'Aerolineas Argentinas',
    'AV': 'Avianca',
    'CM': 'Copa Airlines',
    'LA': 'LATAM Airlines',
    'WS': 'WestJet',
    'BW': 'Caribbean Airlines',
    '4M': 'LATAM Argentina',
    'H2': 'Sky Airlines',
    'Y4': 'Volaris',
    '4O': 'Interjet',
    '5G': 'Global Jet',
    'ZH': 'Shenzhen Airlines',
    'GS': 'Tianjin Airlines',
    'KY': 'Kunming Airlines',
    'SC': 'Shandong Airlines',
    '9C': 'Spring Airlines',
    'JW': 'Vanilla Air',
    'MM': 'Peach Aviation',
    'TR': 'Scoot',
    'FD': 'Thai AirAsia',
    'JQ': 'Jetstar',
    'PG': 'Bangkok Airways',
    'MI': 'SilkAir',
    '3K': 'Jetstar Asia',
    'QG': 'Citilink',
    'AK': 'AirAsia',
    'IX': 'Air India Express',
    'WB': 'RwandAir',
    'KQ': 'Kenya Airways',
    'SW': 'Air Namibia',
    'TM': 'LAM Mozambique',
    
    # Low-Cost Carriers
    'FR': 'Ryanair',
    'U2': 'EasyJet',
    'W6': 'Wizz Air',
    'DY': 'Norwegian Air Shuttle',
    'G4': 'Allegiant Air',
    'NK': 'Spirit Airlines',
    'F9': 'Frontier Airlines',
    'B6': 'JetBlue',
    'WN': 'Southwest Airlines',
    'VY': 'Vueling',
    'HV': 'Transavia',
    'LS': 'Jet2',
    'BY': 'TUI Airways',
    'X3': 'TUIfly',
    'DE': 'Condor',
    'PC': 'Pegasus Airlines',
    'V7': 'Volotea',
    'I2': 'Iberia Express',
    
    # Domestic Carriers
    'AS': 'Alaska Airlines',
    'HA': 'Hawaiian Airlines',
    'SY': 'Sun Country Airlines',
    'YX': 'Republic Airways',
    '9E': 'Endeavor Air',
    'OH': 'PSA Airlines',
    'MQ': 'Envoy Air',
    'OO': 'SkyWest Airlines',
    'YV': 'Mesa Airlines',
    'QX': 'Horizon Air',
    'ZW': 'Air Wisconsin',
    '9K': 'Cape Air',
    'S5': 'Shuttle America',
    'PT': 'Piedmont Airlines',
    
    # New Additional Airlines
    'AD': 'Azul Brazilian Airlines',
    'G3': 'Gol Airlines',
    'O6': 'Avianca Brazil',
    'JJ': 'LATAM Brasil',
    'WM': 'Windward Islands Airways',
    'BN': 'Bahamas Air',
    '7I': 'Insel Air',
    'P4': 'Air Peace',
    'W3': 'Arik Air',
    'DN': 'Norwegian Air Argentina',
    'LV': 'Level Airlines',
    'VB': 'VivaAerobus',
    'LU': 'LAN Express',
    'H8': 'Hesa Airlines',
    'XQ': 'SunExpress',
    'FZ': 'Flydubai',
    'G9': 'Air Arabia',
    'XY': 'Flynas',
    'E5': 'Air Arabia Egypt',
    'OD': 'Malindo Air',
    'JT': 'Lion Air',
    'SL': 'Thai Lion Air',
    'ID': 'Batik Air',
    'Z2': 'AirAsia Philippines',
    'PQ': 'SkyUp Airlines',
    'BT': 'Air Baltic',
    '6E': 'IndiGo',
    'SG': 'SpiceJet',
    'G8': 'GoAir',
    'UK': 'Vistara',
    
    # Cargo Airlines
    '5X': 'UPS Airlines',
    'FX': 'FedEx Express',
    'GEC': 'DHL Air',
    'KZ': 'Nippon Cargo Airlines',
    'CK': 'China Cargo Airlines',
    'CV': 'Cargolux',
    'LH': 'Lufthansa Cargo',
    'KE': 'Korean Air Cargo',
    'SQ': 'Singapore Airlines Cargo',
    'CX': 'Cathay Pacific Cargo',
    
    # Charter Airlines
    'MT': 'Thomas Cook Airlines',
    'TCX': 'Thomas Cook UK',
    'BY': 'TUI Airways',
    'TB': 'TUI fly Belgium',
    'OR': 'TUI fly Netherlands',
    '6B': 'TUI fly Nordic',
    'HQ': 'Thomas Cook Belgium',
    'GM': 'Germania',
    'HF': 'Air Cote d\'Ivoire',
    'XK': 'Air Corsica',
    'D8': 'Norwegian Air International',
    'DI': 'Norwegian Air UK',
}

def get_flight_info(flight_number):
    """Get flight information using the FlightAPI."""
    try:
        # Extract airline code and flight number
        match = re.match(r'([A-Za-z]{2})(\d+)', flight_number)
        if not match:
            return {"error": "Invalid flight number format"}
        
        airline_code = match.group(1).upper()
        flight_num = match.group(2)
        
        # Check if airline code exists
        if airline_code not in AIRLINE_CODES:
            return {"error": f"Unknown airline code: {airline_code}"}
        
        # Get flight information
        flight_data = flight_api.get_flight_info(flight_number)
        if not flight_data:
            return {"error": "No flight information available"}
        
        return flight_data
    except Exception as e:
        return {"error": str(e)}

def info_agent_request(query):
    """Process a query about flight information."""
    try:
        # Extract flight number from query
        flight_number = extract_flight_number(query)
        if not flight_number:
            return {"error": "No flight number found in query"}
        
        # Get flight information
        flight_info = get_flight_info(flight_number)
        if "error" in flight_info:
            return flight_info
        
        # Format the response
        response = {
            "flight_number": flight_number,
            "airline": AIRLINE_CODES.get(flight_number[:2], "Unknown"),
            "status": flight_info.get("status", "Unknown"),
            "departure_time": flight_info.get("departure_time", "Unknown"),
            "arrival_time": flight_info.get("arrival_time", "Unknown"),
            "gate": flight_info.get("gate", "Unknown"),
            "terminal": flight_info.get("terminal", "Unknown")
        }
        
        return response
    except Exception as e:
        return {"error": str(e)}

def extract_flight_number(text):
    """Extract flight number from text using regex."""
    # Pattern to match airline code (2 letters) followed by numbers
    pattern = r'([A-Za-z]{2}\d+)'
    match = re.search(pattern, text)
    return match.group(1) if match else None

def qa_agent_respond(query):
    """Generate a response to a flight information query."""
    try:
        # Extract flight number
        flight_number = extract_flight_number(query)
        if not flight_number:
            return json.dumps({"error": "No flight number found in query"})
        
        # Get flight information
        flight_info = get_flight_info(flight_number)
        if "error" in flight_info:
            return json.dumps(flight_info)
        
        # Format the response
        airline_name = AIRLINE_CODES.get(flight_number[:2], "Unknown")
        response = {
            "answer": f"""Flight {flight_number} ({airline_name}) Information:
Time: {flight_info.get('departure_time', 'Unknown')}
Destination: {flight_info.get('destination', 'Unknown')}
Status: {flight_info.get('status', 'Unknown')}
Gate: {flight_info.get('gate', 'Unknown')}
Terminal: {flight_info.get('terminal', 'Unknown')}
Aircraft: {flight_info.get('aircraft', 'Unknown')}
Estimated Arrival: {flight_info.get('estimated_arrival', 'Unknown')}
Delay: {flight_info.get('delay', 'Unknown')} minutes
Codeshare: {flight_info.get('codeshare', 'Unknown')} ({flight_info.get('codeshare_flight', 'Unknown')})"""
        }
        
        return json.dumps(response)
    except Exception as e:
        return json.dumps({"error": str(e)})
