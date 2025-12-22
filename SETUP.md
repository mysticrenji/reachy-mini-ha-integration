# Reachy Mini Home Assistant Integration - Setup Guide

## Prerequisites

Before installing this integration, ensure you have:

1. **Home Assistant** version 2023.1.0 or newer
2. **Reachy Mini robot** with network connectivity
3. The robot's **IP address** and **port** (default: 50055)
4. **HACS** installed (for easy installation) OR manual file access to Home Assistant

## Installation Methods

### Method 1: HACS (Recommended)

HACS (Home Assistant Community Store) is the easiest way to install and manage custom integrations.

#### Step 1: Add Custom Repository

1. Open Home Assistant
2. Go to **HACS** → **Integrations**
3. Click the **three dots** (⋮) in the top right corner
4. Select **Custom repositories**
5. Add the following:
   - **Repository**: `https://github.com/mysticrenji/reachy-mini-ha-integration`
   - **Category**: `Integration`
6. Click **Add**

#### Step 2: Install the Integration

1. Search for **"Reachy Mini"** in HACS Integrations
2. Click on it and select **Download**
3. Restart Home Assistant

### Method 2: Manual Installation

If you prefer manual installation or don't use HACS:

1. Download the latest release from GitHub
2. Extract the files
3. Copy the `custom_components/reachy_mini` folder to your Home Assistant's `custom_components` directory
   ```
   <config_dir>/custom_components/reachy_mini/
   ```
4. Restart Home Assistant

## Configuration

### Add the Integration

1. In Home Assistant, navigate to:
   - **Settings** → **Devices & Services** → **Integrations**
2. Click the **+ ADD INTEGRATION** button (bottom right)
3. Search for **"Reachy Mini"**
4. Select it from the list

### Configure Connection

You'll be prompted to enter:

- **Host**: The IP address of your Reachy Mini
  - Example: `192.168.1.100`
- **Port**: The port number (default: 50055)
  - Leave as default unless you've configured a different port

Click **Submit** to complete the setup.

## What Gets Created

Once configured, the integration creates the following entities:

### Sensors (3)

1. **Connection Status** (`sensor.reachy_mini_connection_status`)
   - Shows whether the robot is connected or disconnected
   - Values: `connected`, `disconnected`

2. **Battery Level** (`sensor.reachy_mini_battery_level`)
   - Displays the robot's battery percentage
   - Unit: `%`
   - Device Class: Battery

3. **Temperature** (`sensor.reachy_mini_temperature`)
   - Shows the internal temperature
   - Unit: `°C`
   - Device Class: Temperature

### Switches (2)

1. **Compliance Mode** (`switch.reachy_mini_compliance_mode`)
   - Enable/disable compliance mode
   - When ON: Motors are compliant (manually moveable)
   - When OFF: Motors are in standard mode

2. **Torque** (`switch.reachy_mini_torque`)
   - Enable/disable motor torque
   - When ON: Motors are powered
   - When OFF: Motors are unpowered

## Usage Examples

### Dashboard Card

Add this to your Lovelace dashboard:

```yaml
type: entities
title: Reachy Mini Robot
entities:
  - sensor.reachy_mini_connection_status
  - sensor.reachy_mini_battery_level
  - sensor.reachy_mini_temperature
  - switch.reachy_mini_compliance_mode
  - switch.reachy_mini_torque
```

### Automation Example

Create an automation to notify when battery is low:

```yaml
automation:
  - alias: "Reachy Mini Low Battery Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.reachy_mini_battery_level
        below: 20
    action:
      - service: notify.notify
        data:
          message: "Reachy Mini battery is low ({{ states('sensor.reachy_mini_battery_level') }}%)"
```

### Script Example

Create a script to enable compliance mode:

```yaml
script:
  reachy_enable_compliance:
    alias: "Enable Reachy Compliance Mode"
    sequence:
      - service: switch.turn_on
        target:
          entity_id: switch.reachy_mini_compliance_mode
```

## Troubleshooting

### Integration Not Found

**Problem**: Can't find "Reachy Mini" when adding integration

**Solution**:
1. Ensure you've restarted Home Assistant after installation
2. Check that the `custom_components/reachy_mini` folder exists and contains all files
3. Check Home Assistant logs for errors: **Settings** → **System** → **Logs**

### Connection Failed

**Problem**: "Cannot connect to Reachy Mini" error

**Solution**:
1. Verify the IP address is correct
2. Ensure the Reachy Mini is powered on and connected to the network
3. Check that the port is correct (default: 50055)
4. Test network connectivity: `ping <robot-ip>`
5. Ensure no firewall is blocking the connection

### Entities Not Updating

**Problem**: Sensor values not updating

**Solution**:
1. Check the connection status sensor
2. Verify the robot is powered on
3. Check Home Assistant logs for errors
4. Try reloading the integration: **Devices & Services** → **Reachy Mini** → **⋮** → **Reload**

### Removing the Integration

1. Go to **Settings** → **Devices & Services** → **Integrations**
2. Find **Reachy Mini**
3. Click the **three dots** (⋮)
4. Select **Delete**

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/mysticrenji/reachy-mini-ha-integration/issues)
- **Documentation**: [README.md](README.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

## Next Steps

Once configured, you can:
- Add entities to your dashboard
- Create automations based on robot status
- Control the robot through Home Assistant
- Integrate with other Home Assistant devices and services
