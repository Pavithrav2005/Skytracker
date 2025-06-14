from flask import Flask, jsonify, request
from flask_cors import CORS
from agents import qa_agent_respond
import os
import json
from dotenv import load_dotenv
import logging
import sys
from flight_api import FlightAPI

# Configure logging to output to both file and console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('api.log')
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Check if API key is set
api_key = os.getenv('AVIATIONSTACK_API_KEY')
if not api_key:
    logger.error("AVIATIONSTACK_API_KEY environment variable is not set")
    raise ValueError("AVIATIONSTACK_API_KEY environment variable is not set")

app = Flask(__name__)
flight_api = FlightAPI()

# Configure CORS with more permissive settings for development
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-API-Key"],
        "supports_credentials": True
    }
})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is running."""
    return jsonify({"status": "ok", "message": "API is running"}), 200

@app.route('/api/flight/<flight_number>', methods=['GET'])
def get_flight_info(flight_number):
    try:
        logger.info(f"Processing request for flight {flight_number}")
        logger.debug(f"Request headers: {dict(request.headers)}")
        
        # Get API key from headers or environment
        api_key = request.headers.get('X-API-Key') or os.getenv('AVIATIONSTACK_API_KEY')
        if not api_key:
            logger.error("API key not found in headers or environment")
            return jsonify({
                "error": "API key not found",
                "details": "Please provide an API key in the X-API-Key header or set AVIATIONSTACK_API_KEY environment variable",
                "status": 401
            }), 401
        
        # Validate flight number format
        if not flight_number or not isinstance(flight_number, str):
            logger.warning(f"Invalid flight number format: {flight_number}")
            return jsonify({
                "error": "Invalid flight number format",
                "details": "Flight number must be a non-empty string",
                "status": 400
            }), 400
        
        # Create a query for the flight
        query = f"What is the status of flight {flight_number}?"
        logger.info(f"Generated query: {query}")
        
        # Get the response from the QA agent
        response = qa_agent_respond(query)
        logger.info(f"Received response from QA agent: {response}")
        
        # Parse the response
        try:
            response_data = json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse QA agent response: {str(e)}")
            logger.error(f"Raw response: {response}")
            return jsonify({
                "error": "Invalid response format from QA agent",
                "details": str(e),
                "status": 500
            }), 500
        
        # Check if there's an error in the response
        if "error" in response_data:
            logger.error(f"Error in QA agent response: {response_data['error']}")
            return jsonify({
                "error": response_data["error"],
                "details": "Failed to retrieve flight information",
                "status": 404
            }), 404
        
        # Extract the answer from the response
        answer = response_data.get("answer", "")
        if not answer:
            logger.warning("Empty answer received from QA agent")
            return jsonify({
                "error": "No flight information available",
                "details": "The flight information could not be retrieved",
                "status": 404
            }), 404
        
        # Create a structured response
        flight_info = {
            "flight_number": flight_number,
            "departure_time": "Unknown",
            "destination": "Unknown",
            "status": "Unknown",
            "gate": "Unknown",
            "terminal": "Unknown",
            "aircraft": "Unknown",
            "estimated_arrival": "Unknown",
            "delay": "Unknown",
            "codeshare": "Unknown",
            "codeshare_flight": "Unknown"
        }
        
        # Parse the answer to extract information
        try:
            lines = answer.split('\n')
            for line in lines:
                if 'Flight' in line and 'information' in line:
                    continue
                if 'Time:' in line:
                    flight_info['departure_time'] = line.split('Time:')[1].strip()
                elif 'Destination:' in line:
                    flight_info['destination'] = line.split('Destination:')[1].strip()
                elif 'Status:' in line:
                    flight_info['status'] = line.split('Status:')[1].strip()
                elif 'Gate:' in line:
                    flight_info['gate'] = line.split('Gate:')[1].strip()
                elif 'Terminal:' in line:
                    flight_info['terminal'] = line.split('Terminal:')[1].strip()
                elif 'Aircraft:' in line:
                    flight_info['aircraft'] = line.split('Aircraft:')[1].strip()
                elif 'Estimated Arrival:' in line:
                    flight_info['estimated_arrival'] = line.split('Estimated Arrival:')[1].strip()
                elif 'Delay:' in line:
                    delay_str = line.split('Delay:')[1].strip()
                    flight_info['delay'] = delay_str.split()[0]  # Get just the number
                elif 'Codeshare:' in line:
                    codeshare_info = line.split('Codeshare:')[1].strip()
                    if '(' in codeshare_info:
                        flight_info['codeshare'] = codeshare_info.split('(')[0].strip()
                        flight_info['codeshare_flight'] = codeshare_info.split('(')[1].replace(')', '').strip()
            
            logger.info(f"Successfully processed flight info: {flight_info}")
            return jsonify(flight_info)
            
        except Exception as e:
            logger.error(f"Error parsing flight information: {str(e)}")
            return jsonify({
                "error": "Error processing flight information",
                "details": str(e),
                "status": 500
            }), 500
            
    except Exception as e:
        logger.error(f"Unexpected error processing flight info: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e),
            "status": 500
        }), 500

@app.route('/api/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        user_query = data.get('query', '')
        if not user_query:
            return jsonify({'error': 'No query provided'}), 400
        response = qa_agent_respond(user_query)
        try:
            response_data = json.loads(response)
        except Exception:
            response_data = {'answer': response}
        return jsonify(response_data)
    except Exception as e:
        logger.error(f"Error in /api/query: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

if __name__ == '__main__':
    try:
        # Load environment variables
        load_dotenv()
        
        # Check if API key is set
        if not os.getenv('AVIATIONSTACK_API_KEY'):
            logger.warning("AVIATIONSTACK_API_KEY environment variable is not set")
            print("⚠️ Warning: AVIATIONSTACK_API_KEY environment variable is not set.")
            print("Please set your API key using:")
            print("Windows PowerShell: $env:AVIATIONSTACK_API_KEY='your_api_key'")
            print("Linux/Mac: export AVIATIONSTACK_API_KEY='your_api_key'")
            print("Note: The API will still work if the key is provided in the request headers.")
        
        logger.info("Starting Flask server...")
        # Run the Flask app
        app.run(debug=True, port=5000, host='0.0.0.0')
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        sys.exit(1)