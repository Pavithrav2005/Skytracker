# Airline Assistant Backend

This README file provides documentation for the backend part of the Airline Assistant application.

## Overview

The Airline Assistant is a real-time chatbot application that provides users with information about flights using the AviationStack API. The backend is built using Python and handles user queries, processes responses, and interfaces with the AviationStack API.

## Project Structure

```
airline-assistant/
├── backend/
│   ├── main.py                # Main logic for the airline assistant application
│   ├── agents/
│   │   └── qa_agent_respond.py # Logic for responding to user queries
│   ├── requirements.txt        # Python dependencies
│   └── README.md               # Documentation for the backend
└── frontend/                   # Frontend application (React)
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd airline-assistant/backend
   ```

2. **Create a virtual environment (optional but recommended):**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Ensure that the `AVIATIONSTACK_API_KEY` environment variable is set with your AviationStack API key. You can do this by adding the following line to your environment configuration:
   - Windows PowerShell: `$env:AVIATIONSTACK_API_KEY='your_api_key'`
   - Linux/Mac: `export AVIATIONSTACK_API_KEY='your_api_key'`

5. **Run the application:**
   ```
   python main.py
   ```

## Usage

- The application will start and display a welcome message.
- Users can interact with the chatbot by typing queries related to flight information.
- The chatbot will respond with real-time data fetched from the AviationStack API.

## Dependencies

The backend requires the following Python packages:
- Flask
- requests
- python-dotenv

These packages are listed in the `requirements.txt` file.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.