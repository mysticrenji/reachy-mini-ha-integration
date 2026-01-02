# Contributing to Reachy Mini Home Assistant Integration

Thank you for your interest in contributing to the Reachy Mini Home Assistant Integration!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/mysticrenji/reachy-mini-ha-integration.git
   cd reachy-mini-ha-integration
   ```

2. Install Home Assistant development environment (optional, for testing):
   ```bash
   pip install homeassistant
   ```

3. Link the custom component to your Home Assistant instance:
   ```bash
   ln -s $(pwd)/custom_components/reachy_mini ~/.homeassistant/custom_components/reachy_mini
   ```

## Code Structure

```
custom_components/reachy_mini/
├── __init__.py          # Component initialization
├── config_flow.py       # UI configuration flow
├── const.py            # Constants
├── manifest.json       # Integration metadata
├── sensor.py           # Sensor entities
├── switch.py           # Switch entities
├── camera.py           # Camera entities
├── strings.json        # UI strings
├── icons.json          # Icon definitions
└── translations/       # Localization files
    └── en.json
```

## Adding New Features

### Adding a New Sensor

1. Add sensor class to `sensor.py`
2. Inherit from `ReachyMiniSensorBase`
3. Implement the `async_update` method
4. Add to the sensors list in `async_setup_entry`

### Adding a New Switch

1. Add switch class to `switch.py`
2. Inherit from `ReachyMiniSwitchBase`
3. Implement `async_turn_on` and `async_turn_off` methods
4. Add to the switches list in `async_setup_entry`

### Adding a New Camera

1. Add camera class to `camera.py`
2. Inherit from `Camera`
3. Implement `async_camera_image` and `stream_source` methods
4. Add to the cameras list in `async_setup_entry`

## Integration with Reachy Mini SDK

The integration uses the `reachy-mini` SDK package to communicate with the Reachy Mini robot. The robot uses a **client-server architecture** where:

- **The Daemon (Server)**: Runs on the robot, handles hardware I/O, and exposes a REST API (port 8000) and Zenoh messaging
- **The SDK (Client)**: Connects to the daemon over the network

Example usage:
```python
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose
import numpy as np

# Connect to robot (daemon running on host:port)
with ReachyMini(connection_mode="network") as mini:
    # Get current state
    state = mini.state
    
    # Move the head
    mini.goto_target(
        head=create_head_pose(z=10, roll=15, mm=True, degrees=True),
        antennas=np.deg2rad([45, 45]),
        duration=2.0
    )
    
    # Get camera frame
    frame = mini.media.get_frame()
    
    # Get sensor data
    battery = state.get('battery_level')
```

**Alternative: REST API**
For simpler integrations, you can use the REST API directly:
```python
import requests

# Get full state
response = requests.get(f'http://{host}:8000/api/state/full')
state = response.json()
```

## Testing

1. Test with a real Reachy Mini robot if available
2. Test the configuration flow in Home Assistant UI
3. Verify all sensors and switches appear correctly
4. Test enable/disable functionality

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to all functions and classes
- Use async/await for all Home Assistant operations

## SDK Resources

- **GitHub**: https://github.com/pollen-robotics/reachy_mini
- **PyPI**: https://pypi.org/project/reachy-mini/
- **SDK Documentation**: See the SDK docs folder in the GitHub repo
- **REST API**: `http://localhost:8000/docs` (when daemon is running)

## Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Resources

- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Reachy Mini Documentation](https://docs.pollen-robotics.com/)
- [HACS Documentation](https://hacs.xyz/)
