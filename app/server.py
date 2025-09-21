from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/people')
def people():
    return jsonify([
        {"name": "Alice", "conversations": 12, "tone": "positive", "alerts": 3},
        {"name": "Bob", "conversations": 8, "tone": "neutral", "alerts": 0}
    ])

@app.route('/conversations')
def conversations():
    return jsonify([
        {"time": "10:00 AM", "flags": ["urgent"], "sentiment": "negative", "summary": "Disagreement noted"},
        {"time": "2:00 PM", "flags": [], "sentiment": "positive", "summary": "Friendly check-in"}
    ])

if __name__ == '__main__':
    app.run(debug=True)
