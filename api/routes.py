import os
import time
import csv
from flask import Blueprint, jsonify, request
from services.first_aid_service import FirstAidService

# Create a Blueprint for the API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Store the config for use in routes
_config = None
LOG_FILE = "response_logs.csv"

def init_routes(config):
    """Initialize the routes with the given config"""
    global _config
    _config = config
  # Ensure the log file exists with proper headers
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Query", "Response", "Response Length", "Response Time (seconds)"])

    return api_bp

@api_bp.route('/health', methods=['GET'])
def health_check():
    """API endpoint to check if the service is running"""
    return jsonify({
        "status": "healthy", 
        "message": "First Aid Recommendation API is running"
    })

@api_bp.route('/recommend', methods=['POST'])
def get_recommendation():
    """API endpoint to get first aid recommendations"""
    # Get the query from the request
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request data"}), 400
    
    query = data['query']
    
    try:
        # Get the recommendation
        # Measure response time
        start_time = time.time()
        response = FirstAidService.get_recommendation(query, _config)
        response_time = time.time() - start_time
        response_length = len(response.split())
        
# Log the data
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([query, response, response_length, response_time])

        return jsonify({
            "query": query,
            "recommendation": response if response else "I'm here to help, but I didn't understand that.",
            "response_length": response_length,
            "response_time": response_time
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@api_bp.route('/logs', methods=['GET'])
def get_logs():
    """API endpoint to retrieve the logged response data"""
    try:
        if not os.path.exists(LOG_FILE):
            return jsonify({"message": "No logs found"}), 404

        logs = []
        with open(LOG_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                logs.append(row)

        return jsonify({"logs": logs}), 200
    except Exception as e:
        print(f"Error retrieving logs: {str(e)}")
        return jsonify({"error": f"An error occurred while retrieving logs: {str(e)}"}), 500
