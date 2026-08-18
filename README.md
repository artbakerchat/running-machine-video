# Running Machine Video Sync

A Python web application that synchronizes video playback with treadmill sensor data. The video playback speed automatically adjusts based on your running speed, creating an immersive experience where the video background moves faster as you run faster.

## Features

- 🎥 **Real-time Video Sync**: Video playback speed adapts to your running speed
- 📊 **Live Statistics**: Track speed, distance, and playback rate
- 🏃 **Treadmill Integration**: Accepts sensor data from treadmill APIs
- 🧪 **Sensor Simulator**: Built-in simulator for testing without a physical treadmill
- 💻 **Web-based**: Access from any browser
- ⚡ **Real-time Updates**: Smooth synchronization via AJAX polling

## Project Structure

```
running-machine-video/
├── app.py                    # Flask backend server
├── sensor_simulator.py       # Treadmill sensor simulator for testing
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Frontend UI
├── static/
│   └── videos/
│       └── running.mp4      # Sample video file (you need to add this)
└── README.md                # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- A pre-recorded running/outdoor video (MP4 format)

### Setup Steps

1. **Navigate to project directory**:
   ```bash
   cd ~/Downloads/running-machine-video
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your video file**:
   - Create `static/videos/` directory
   - Place your running video as `static/videos/running.mp4`
   - Video format: MP4, H.264 codec recommended

5. **Run the Flask server**:
   ```bash
   python app.py
   ```

   The server will start at `http://localhost:5000`

## Usage

### Option 1: Manual Testing (Simulation)

1. Open your browser and go to `http://localhost:5000`
2. Enter a speed value (0-30 km/h) in the "Simulated Speed" field
3. Click "Start Simulation"
4. Watch the video playback speed adjust based on your input
5. Click "Stop Simulation" to pause

### Option 2: Automated Sensor Simulation

In a separate terminal (with venv activated):

```bash
python sensor_simulator.py
```

This runs three different test scenarios:
- **Test 1**: Constant speed (10 km/h for 15 seconds)
- **Test 2**: Speed progression (gradual speed changes)
- **Test 3**: Interval training (work/rest cycles)

Watch the UI update in real-time as the simulator sends data.

### Option 3: Real Treadmill Integration

To connect a real treadmill:

1. **Modify the treadmill sensor connection** in your treadmill's API/SDK
2. **Send POST requests** to the backend:

```bash
curl -X POST http://localhost:5000/api/sensor/data \
  -H "Content-Type: application/json" \
  -d '{"speed": 12.5, "distance": 150.0}'
```

Replace `12.5` with actual speed (km/h) and `150.0` with distance (meters).

## How It Works

### Speed-to-Playback Mapping

The video playback speed is calculated based on running speed:

- **Base Speed**: 10 km/h → 1.0x playback (normal speed)
- **Faster speeds** (e.g., 15 km/h) → Higher playback rate (e.g., 1.5x)
- **Slower speeds** (e.g., 5 km/h) → Lower playback rate (e.g., 0.5x)
- **Limits**: Playback constrained between 0.5x and 2.0x

**Formula**:
```
playback_speed = (running_speed_kmh / 10) 
playback_speed = clamp(playback_speed, 0.5, 2.0)
```

### Architecture

```
┌─────────────────┐
│  Treadmill      │
│   Sensor API    │
└────────┬────────┘
         │ POST /api/sensor/data
         ↓
┌─────────────────┐
│   Flask Backend │
│   (app.py)      │
└────────┬────────┘
         │ GET /api/running-state
         ↓
┌─────────────────┐
│   Browser UI    │
│   (index.html)  │
└─────────────────┘
         │ Adjusts video.playbackRate
         ↓
     [Video Player]
```

## API Endpoints

### POST `/api/sensor/data`
Receive treadmill sensor data.

**Request**:
```json
{
  "speed": 12.5,
  "distance": 500.0
}
```

**Response**:
```json
{
  "status": "success",
  "received": {
    "speed": 12.5,
    "distance": 500.0,
    "timestamp": "2024-01-15T10:30:45.123456",
    "is_running": true
  }
}
```

### GET `/api/running-state`
Get current running state.

**Response**:
```json
{
  "speed": 12.5,
  "distance": 500.0,
  "is_running": true,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### GET `/api/video-config`
Get video configuration.

**Response**:
```json
{
  "video_path": "/static/videos/running.mp4",
  "base_speed": 10,
  "max_playback_speed": 2.0,
  "min_playback_speed": 0.5
}
```

## Video Requirements

For best results, use:
- **Format**: MP4 with H.264 video codec
- **Duration**: 2-5 minutes recommended
- **Resolution**: 1080p or higher
- **Frame Rate**: 30 fps
- **Content**: Steady outdoor running/jogging footage (minimal camera movement)

### Finding Sample Videos

Free stock video sources:
- **Pexels** (pexels.com)
- **Pixabay** (pixabay.com)
- **Unsplash** (unsplash.com)

Search for: "running", "jogging", "outdoor running", "cardio"

## Configuration

Edit `app.py` to customize:

```python
# In app.py
BASE_SPEED = 10       # km/h - speed that plays video at 1.0x
MAX_PLAYBACK = 2.0    # Maximum playback rate
MIN_PLAYBACK = 0.5    # Minimum playback rate
```

Edit playback limits in `templates/index.html`:

```javascript
const BASE_SPEED = 10;      // km/h
const MAX_PLAYBACK = 2.0;
const MIN_PLAYBACK = 0.5;
```

## Troubleshooting

### Video doesn't play
- Ensure video file exists at `static/videos/running.mp4`
- Check browser console for errors (F12)
- Try with a different video format (WebM, OGG)

### Playback not syncing
- Check browser console for JavaScript errors
- Verify backend is running: `http://localhost:5000/api/running-state`
- Clear browser cache and reload

### Backend connection errors
- Ensure Flask server is running
- Check port 5000 is not in use
- Verify firewall allows localhost connections

### Sensor data not received
- Test with curl: `curl http://localhost:5000/api/running-state`
- Check Content-Type is `application/json`
- Verify JSON format in POST request

## Performance Tips

- Use a shorter video (30-60 seconds) for faster loop
- Close other browser tabs to reduce CPU usage
- Use hardware acceleration in browser settings
- Test with different BASE_SPEED values for your needs

## Future Enhancements

- [ ] Add real-time video effect (motion blur, brightness)
- [ ] Support multiple video tracks (indoor, outdoor, etc.)
- [ ] Leaderboard and statistics tracking
- [ ] Mobile app integration
- [ ] Support for incline/resistance adjustment
- [ ] Audio sync (footsteps, breathing sound effects)

## License

MIT License - Feel free to use and modify

## Support

For issues or questions, add debug output to `app.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Then check terminal output for detailed logs.
