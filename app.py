from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime
import threading
import time

app = Flask(__name__)
CORS(app)

# Store current running state
running_state = {
    'speed': 0.0,  # km/h or m/s
    'distance': 0.0,  # meters
    'timestamp': datetime.now(),
    'is_running': False
}

# Lock for thread-safe access
state_lock = threading.Lock()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/sensor/data', methods=['POST'])
def receive_sensor_data():
    """
    Receive treadmill sensor data
    Expected JSON: {"speed": float, "distance": float}
    speed in km/h, distance in meters
    """
    try:
        data = request.json
        with state_lock:
            running_state['speed'] = float(data.get('speed', 0))
            running_state['distance'] = float(data.get('distance', 0))
            running_state['timestamp'] = datetime.now()
            running_state['is_running'] = running_state['speed'] > 0
        
        return jsonify({'status': 'success', 'received': running_state}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/running-state', methods=['GET'])
def get_running_state():
    """Get current running state for frontend"""
    with state_lock:
        state = running_state.copy()
        state['timestamp'] = state['timestamp'].isoformat()
    return jsonify(state), 200

@app.route('/api/video-config', methods=['GET'])
def get_video_config():
    """Return video configuration"""
    config = {
        'video_path': '/static/videos/running.mp4',
        'base_speed': 10,  # km/h - baseline speed for video
        'max_playback_speed': 2.0,  # Max playback rate
        'min_playback_speed': 0.5   # Min playback rate
    }
    return jsonify(config), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
