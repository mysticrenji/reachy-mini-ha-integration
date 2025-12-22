# Reachy Mini Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

This is a custom Home Assistant integration for the Reachy Mini robot by Pollen Robotics.

## Features

### Sensors
- **Connection Status**: Monitor the connection state of your Reachy Mini
- **Battery Level**: Track the battery percentage
- **Temperature**: Monitor internal temperature

### Switches
- **Compliance Mode**: Enable/disable compliance mode for manual manipulation
- **Torque**: Enable/disable motor torque

### Camera
- **Teleop Camera**: Live video feed from the robot's camera with streaming support

## Installation

### Via HACS (recommended)
1. Add this repository as a custom repository in HACS
2. Search for "Reachy Mini" in HACS integrations
3. Install the integration
4. Restart Home Assistant

### Manual Installation
1. Copy the `custom_components/reachy_mini` folder to your config directory
2. Restart Home Assistant

## Configuration

Add the integration through the Home Assistant UI:
1. Go to Configuration → Integrations
2. Click the + button
3. Search for "Reachy Mini"
4. Enter your Reachy Mini's IP address and port (default: 50055)

## Requirements

- Home Assistant 2023.1.0 or later
- Reachy Mini robot with network connectivity
- Reachy Mini Python SDK (installed automatically)

## Support

For issues and questions, please use the [GitHub issue tracker](https://github.com/mysticrenji/reachy-mini-ha-integration/issues).
