# Import required libraries
from flask import Flask, jsonify
import requests
import time
from datetime import datetime
from collections import deque
import threading

DATA_COLLECTION_INTERVAL = 10  # 10 seconds
MIN_ALTITUDE_THRESHOLD = 160  # Threshold for warning message
LOW_ORBIT_WARNING_INTERVAL = 60 # 1 minute in seconds

app = Flask(__name__)
stats_buffer = deque(maxlen=30)  # Number of data points to keep (5 minutes with 10-second interval)
health_buffer = deque(maxlen=6) # Number of data points to keep (1 minute with 10-second interval)
low_orbit_warning_time = 0 # Initialize current low orbit warning time

# Function to fetch real-time satellite data from the link
def get_satellite_data():
    url = 'https://api.cfast.dev/satellite/'
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                # Convert ISO 8601 timestamp to a datetime object
                timestamp_str = data.get("last_updated")
                if timestamp_str:
                    data["last_updated"] = datetime.fromisoformat(timestamp_str).timestamp()
                    stats_buffer.append(data)
                    health_buffer.append(data)
                    print(data)
                else:
                    print("Timestamp not found in the API response.")
            else:
                print(f"API request failed with status code: {response.status_code}")
        except Exception as e:
            print(f"Error occurred during data collection: {e}")

        time.sleep(DATA_COLLECTION_INTERVAL)

def calculate_stats():
    data = [record['altitude'] for record in stats_buffer]
    min_altitude = min(data)
    max_altitude = max(data)
    avg_altitude = sum(data) / len(data)
    return min_altitude, max_altitude, avg_altitude

def calculate_health(data_buffer, threshold, interval, low_orbit_warning_time):
    avg_altitude_last_minute = get_average_altitude(data_buffer)

    print("Average altitude for the last minute:", avg_altitude_last_minute)

    if avg_altitude_last_minute < threshold:
        low_orbit_warning_time = time.time()
        return "WARNING: RAPID ORBITAL DECAY IMMINENT"
    else:
        return "Sustained Low Earth Orbit Resumed" if time.time() - low_orbit_warning_time <= interval else "Altitude is A-OK"

def get_average_altitude(data):
    if not data:
        return 0  # Return 0 if data is empty
    return sum(record["altitude"] for record in data) / len(data)

# /stats endpoint to get statistics for the last 5 minutes
@app.route('/stats', methods=['GET'])
def get_stats():
    min_altitude, max_altitude, avg_altitude = calculate_stats()
    stats = {
        "min_altitude": min_altitude,
        "max_altitude": max_altitude,
        "avg_altitude": avg_altitude
    }
    return jsonify(stats), 200

# /stats endpoint to get health status for the last minute
@app.route('/health', methods=['GET'])
def get_health():
    global low_orbit_warning_time

    data_last_minute = list(health_buffer)
    result_message = calculate_health(data_last_minute, MIN_ALTITUDE_THRESHOLD, LOW_ORBIT_WARNING_INTERVAL, low_orbit_warning_time)

    return jsonify({"message": result_message}), 200


if __name__ == '__main__':

    # Start the data collection in a separate thread
    data_collection_thread = threading.Thread(target=get_satellite_data)
    data_collection_thread.daemon = True  # Allow the thread to terminate when the main thread exits
    data_collection_thread.start()
    data_collection_started = True

    # Start the Flask app to serve the API endpoints
    app.run(debug=True, use_reloader=False)
        
