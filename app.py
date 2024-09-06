from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests if the frontend is hosted separately

# Sample tourist spots data
tourist_spots = [
    {"name": "Maldives", "keywords": ["beaches", "relaxation", "nature"]},
    {"name": "Paris", "keywords": ["museums", "art", "culture"]},
    {"name": "New York", "keywords": ["city", "shopping", "adventure"]},
    {"name": "Bali", "keywords": ["beaches", "hiking", "nature"]},
    {"name": "Tokyo", "keywords": ["technology", "city", "culture"]},
    {"name": "Swiss Alps", "keywords": ["hiking", "nature", "adventure"]},
]

# Helper function to match user preferences with tourist spots
def get_recommendations(activities, travel_type):
    matched_spots = []
    keywords = activities.lower().split() + [travel_type.lower()]
    
    for spot in tourist_spots:
        # Check if any user keywords match the spot keywords
        if any(keyword in spot["keywords"] for keyword in keywords):
            matched_spots.append(spot["name"])

    return matched_spots

# Route to handle form data and return recommendations
@app.route('/submit', methods=['POST'])
def submit():
    # Get data from the frontend
    data = request.get_json()
    destination = data.get('destination', '')
    activities = data.get('activities', '')
    travel_type = data.get('travelType', '')

    # Validate the input data
    if not destination or not activities or not travel_type:
        return jsonify({"error": "All fields are required!"}), 400

    # Get recommendations based on activities and travel type
    recommendations = get_recommendations(activities, travel_type)

    # Return recommendations as JSON
    if recommendations:
        return jsonify({"recommendations": recommendations}), 200
    else:
        return jsonify({"message": "No recommendations found based on your preferences."}), 200

# Root route to check if the server is running
@app.route('/')
def home():
    return 'Travel Recommendation API is running!'

if __name__ == '__main__':
    app.run(debug=True)