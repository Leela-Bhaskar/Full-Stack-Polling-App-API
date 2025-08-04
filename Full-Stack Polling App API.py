# main.py
from flask import Flask, request, jsonify
import uuid

# Initialize the Flask application
app = Flask(__name__)

# In-memory data store for polls.
# In a real-world application, you would use a database like PostgreSQL or MongoDB.
polls = {}

# --- Helper Functions ---

def generate_id():
    """Generates a unique string ID."""
    return str(uuid.uuid4())

# --- API Endpoints ---

@app.route('/poll', methods=['POST'])
def create_poll():
    """
    Creates a new poll.
    Expects a JSON payload with a "question" and a list of "options".
    Example:
    {
        "question": "What is your favorite programming language?",
        "options": ["Python", "JavaScript", "Go", "Rust"]
    }
    """
    data = request.get_json()

    # --- Input Validation ---
    if not data or 'question' not in data or 'options' not in data:
        return jsonify({"error": "Missing 'question' or 'options' in request body"}), 400
    if not isinstance(data['question'], str) or not data['question'].strip():
        return jsonify({"error": "'question' must be a non-empty string"}), 400
    if not isinstance(data['options'], list) or len(data['options']) < 2:
        return jsonify({"error": "'options' must be a list with at least two choices"}), 400

    # --- Poll Creation ---
    poll_id = generate_id()
    new_poll = {
        "question": data['question'],
        "options": {str(i): option for i, option in enumerate(data['options'])},
        "votes": {str(i): 0 for i in range(len(data['options']))}
    }
    polls[poll_id] = new_poll

    return jsonify({
        "message": "Poll created successfully!",
        "poll_id": poll_id,
        "poll_data": new_poll
    }), 201

@app.route('/poll/<string:poll_id>', methods=['GET'])
def get_poll(poll_id):
    """
    Retrieves the results of a specific poll.
    """
    poll = polls.get(poll_id)

    if not poll:
        return jsonify({"error": "Poll not found"}), 404

    # --- Format Results ---
    results = {
        "question": poll["question"],
        "results": [
            {"option": text, "votes": poll["votes"][option_id]}
            for option_id, text in poll["options"].items()
        ]
    }

    return jsonify({
        "poll_id": poll_id,
        "poll_results": results
    }), 200

@app.route('/poll/<string:poll_id>/vote/<string:option_id>', methods=['POST'])
def vote(poll_id, option_id):
    """
    Records a vote for a specific option in a poll.
    """
    poll = polls.get(poll_id)

    # --- Validation ---
    if not poll:
        return jsonify({"error": "Poll not found"}), 404
    if option_id not in poll['options']:
        return jsonify({"error": "Invalid option ID"}), 400

    # --- Record Vote ---
    poll['votes'][option_id] += 1

    return jsonify({
        "message": "Vote cast successfully!",
        "poll_id": poll_id,
        "voted_for_option": option_id
    }), 200

@app.route("/")
def home():
    return """
        <div style='font-family:sans-serif;max-width:600px;margin:40px auto;padding:24px;border-radius:12px;background:#f9f9f9;box-shadow:0 2px 8px #0001;'>
            <h1 style='color:#4CAF50;'>🗳️ Welcome to the <span style="color:#2196F3;">Polling API</span>!</h1>
            <p>Create and vote in live polls with ease. Try these endpoints:</p>
            <ul style='font-size:1.1em;'>
                <li><b>POST</b> <code>/poll</code> – <span style="color:#888;">Create a new poll</span></li>
                <li><b>GET</b> <code>/poll/&lt;poll_id&gt;</code> – <span style="color:#888;">Get poll results</span></li>
                <li><b>POST</b> <code>/poll/&lt;poll_id&gt;/vote/&lt;option_id&gt;</code> – <span style="color:#888;">Vote for an option</span></li>
            </ul>
            <h3>🚀 Quick Start Example</h3>
            <pre style='background:#eee;padding:10px;border-radius:6px;'>
curl -X POST http://127.0.0.1:5000/poll -H "Content-Type: application/json" -d '{"question":"Best language?","options":["Python","JavaScript"]}'
            </pre>
            <p style='color:#888;font-size:0.95em;'>Made with Flask &amp; ❤️</p>
        </div>
    """

# --- Main Execution ---

if __name__ == '__main__':
    # To run this app:
    # 1. Make sure you have Flask installed: pip install Flask
    # 2. Run the script: python main.py
    # The app will be running on http://127.0.0.1:5000
    app.run(debug=True, host='0.0.0.0', port=5000)
