from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from agents.qa_agent_respond import qa_agent_respond

app = Flask(__name__)

load_dotenv()

@app.route('/api/query', methods=['POST'])
def query():
    user_query = request.json.get('query')
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    response = qa_agent_respond(user_query)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)