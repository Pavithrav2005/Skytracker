# Airline Assistant Project

This project is an Airline Assistant application that provides real-time information about flights using the AviationStack API. It consists of a backend service built with Python and a frontend interface developed with React.

## Project Structure

```
airline-assistant
├── backend
│   ├── main.py                # Main logic for the airline assistant application
│   ├── agents
│   │   └── qa_agent_respond.py # Logic for responding to user queries
│   ├── requirements.txt        # Python dependencies for the backend
│   └── README.md               # Documentation for the backend
├── frontend
│   ├── public
│   │   └── index.html          # Main HTML entry point for the frontend
│   ├── src
│   │   ├── App.js              # Main component of the React application
│   │   ├── Chatbot.js          # Chatbot component for user interactions
│   │   ├── api.js              # Functions to interact with the backend API
│   │   └── index.js            # Entry point for the React application
│   ├── package.json            # Configuration file for npm
│   └── README.md               # Documentation for the frontend
└── README.md                   # Overview of the entire project
```

## Backend Setup

1. Navigate to the `backend` directory.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set the `AVIATIONSTACK_API_KEY` environment variable with your API key.
4. Run the application:
   ```
   python main.py
   ```

## Frontend Setup

1. Navigate to the `frontend` directory.
2. Install the required dependencies:
   ```
   npm install
   ```
3. Start the React application:
   ```
   npm start
   ```

## Usage

- Use the chatbot interface in the frontend to ask about flight statuses and other airline-related queries.
- The backend processes these queries and fetches the necessary information from the AviationStack API.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.