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

The integration uses the `reachy2-sdk-api` package to communicate with the Reachy Mini robot via gRPC. This is a lightweight package that provides protocol buffer interfaces without heavy dependencies like OpenCV, making it suitable for containerized deployments.

Example usage:
```python
from reachy2_sdk_api import reachy_pb2, reachy_pb2_grpc
import grpc

# Connect to robot
channel = grpc.insecure_channel(f'{host}:{port}')
stub = reachy_pb2_grpc.ReachyServiceStub(channel)

# Make gRPC calls to control the robot
# Example: Get robot info, control components, etc.
# See the reachy2-sdk-api documentation for available services
```

**Note on package choice:**
- **`reachy2-sdk-api`** (required): Provides gRPC protocol buffer interfaces. Use this for the integration implementation.
- **`reachy2-sdk`** (optional): High-level Python SDK with image processing and math utilities. Only needed for local development/testing if you need to process camera images or use advanced features. Do NOT add as a requirement to manifest.json as it has heavy dependencies (opencv-python, numpy) that prevent installation in containerized environments.

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
