# Reachy Mini Home Assistant Integration

Home Assistant custom integration for Reachy Mini robot by Pollen Robotics.

This integration allows you to monitor and control your Reachy Mini robot through Home Assistant.

## Features

- **Sensors**:
  - Connection status monitoring
  - Battery level monitoring
  - Temperature monitoring

- **Switches**:
  - Compliance mode control
  - Torque enable/disable

- **Camera**:
  - Live camera feed from Reachy Mini's teleop camera
  - Stream support for real-time video viewing

## Installation

### HACS Installation (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/mysticrenji/reachy-mini-ha-integration`
6. Select category: "Integration"
7. Click "Add"
8. Find "Reachy Mini" in the integration list and click "Download"
9. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/reachy_mini` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## Configuration

1. In Home Assistant, go to **Configuration** > **Integrations**
2. Click the **+ Add Integration** button
3. Search for "Reachy Mini"
4. Enter your Reachy Mini connection details:
   - **Host**: IP address of your Reachy Mini robot
   - **Port**: Port number (default: 8000 for REST API)
5. Click **Submit**

## Usage

Once configured, the integration will create:

### Sensors
- `sensor.reachy_mini_connection_status` - Shows if the robot is connected
- `sensor.reachy_mini_battery_level` - Shows battery percentage
- `sensor.reachy_mini_temperature` - Shows internal temperature

### Switches
- `switch.reachy_mini_compliance_mode` - Toggle compliance mode
- `switch.reachy_mini_torque` - Toggle motor torque

### Camera
- `camera.reachy_mini_teleop_camera` - Live video feed from the robot's camera

## Requirements

- Home Assistant 2023.1.0 or newer
- Reachy Mini robot with network connectivity
- Reachy Mini Python SDK (automatically installed)

> **Note**: This integration uses the `reachy-mini` SDK package. The robot uses a client-server architecture where the daemon runs on the robot (exposing a REST API on port 8000 and Zenoh messaging) and the SDK connects to it over the network.

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/mysticrenji/reachy-mini-ha-integration/issues).

## License

This project is licensed under the MIT License.

## Credits

Developed for integration with [Reachy Mini](https://www.pollen-robotics.com/) by Pollen Robotics.
