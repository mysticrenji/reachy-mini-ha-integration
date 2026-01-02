# Copilot Instructions for Reachy Mini Home Assistant Integration

## Project Overview

This is a **Home Assistant custom integration** for the Reachy Mini robot by Pollen Robotics. It provides sensors, switches, and camera entities to monitor and control the robot via Home Assistant's UI.

**Architecture**: Standard Home Assistant custom component following the platform-based entity model. Each entity type (sensor/switch/camera) lives in its own module and inherits from Home Assistant base classes.

## Critical Context

### Reachy Mini SDK Architecture

**IMPORTANT**: This integration uses the `reachy-mini` SDK package (from PyPI). The Reachy Mini robot uses a **client-server architecture**:

- **The Daemon (Server)**: Runs on the robot at `host:8000` (default port 50055 is NOT used - REST API is on port 8000)
  - Handles hardware I/O, safety checks, and sensor reading
  - Exposes REST API: `http://host:8000/api/*`
  - Uses Zenoh for real-time messaging
  
- **The SDK (Client)**: Python package that connects to the daemon
  - Import: `from reachy_mini import ReachyMini`
  - Auto-detects connection mode (localhost vs network)

**Connection Options**:
```python
# Auto mode (recommended) - detects if running locally or remote
with ReachyMini() as mini:
    pass

# Force localhost (for USB/local daemon)
with ReachyMini(connection_mode="localhost_only") as mini:
    pass

# Force network discovery
with ReachyMini(connection_mode="network") as mini:
    pass
```

**Alternative: REST API** (simpler for basic queries):
```python
import requests
response = requests.get(f'http://{host}:8000/api/state/full')
state = response.json()
```

See [CONTRIBUTING.md](CONTRIBUTING.md#integration-with-reachy-mini-sdk) for detailed SDK usage examples.

### Entity Architecture Pattern

All entities follow this base class pattern:

1. **Base classes** inherit from Home Assistant entity types and define:
   - `device_info` property (groups entities under one device)
   - Connection parameters (`_host`, `_port`)
   - Entry reference for unique IDs

2. **Concrete entity classes** implement:
   - `async_update()` for sensors
   - `async_turn_on()`/`async_turn_off()` for switches
   - `async_camera_image()`/`stream_source()` for cameras

Example from [sensor.py](custom_components/reachy_mini/sensor.py):
```python
class ReachyMiniSensorBase(SensorEntity):
    def __init__(self, entry: ConfigEntry, host: str, port: int):
        self._entry = entry
        self._host = host
        self._port = port
        self._attr_has_entity_name = True
    
    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, f"{self._host}:{self._port}")},
            name=f"Reachy Mini ({self._host})",
            # ...
        )
```

### Platform Registration Flow

1. [\_\_init\_\_.py](custom_components/reachy_mini/__init__.py) stores host/port in `hass.data[DOMAIN][entry.entry_id]`
2. Each platform's `async_setup_entry()` reads from `hass.data`
3. Entities are instantiated with connection info and added via `async_add_entities()`

### Configuration Flow

[config_flow.py](custom_components/reachy_mini/config_flow.py) handles UI setup:
- Schema requires `CONF_HOST` and optional `CONF_PORT` (defaults to 50055)
- `async_set_unique_id()` prevents duplicate integrations for same host:port
- Production TODO: Add actual connection validation (currently placeholder)

## Development Workflows

### Testing Locally

Link custom component to HA instance:
```bash
ln -s $(pwd)/custom_components/reachy_mini ~/.homeassistant/custom_components/reachy_mini
```

Restart Home Assistant to load changes.

### Adding New Entities

1. **Sensor**: Add class to [sensor.py](custom_components/reachy_mini/sensor.py), inherit from `ReachyMiniSensorBase`, implement `async_update()`, add to `sensors` list
2. **Switch**: Add class to [switch.py](custom_components/reachy_mini/switch.py), inherit from `ReachyMiniSwitchBase`, implement turn on/off methods
3. **Camera**: Add class to [camera.py](custom_components/reachy_mini/camera.py), inherit from `Camera`, implement image/stream methods

Update unique IDs to follow pattern: `{entry.entry_id}_{entity_type}_{name}`

### HACS Compatibility

- [hacs.json](hacs.json) defines HACS metadata (minimum HA version: 2023.1.0)
- [manifest.json](custom_components/reachy_mini/manifest.json) must specify `version`, `requirements`, `iot_class` (currently: `local_polling`)

## Project-Specific Patterns

### Constants

[const.py](custom_components/reachy_mini/const.py) centralizes:
- `DOMAIN = "reachy_mini"` (used for `hass.data` namespacing)
- `SCAN_INTERVAL = 30` (sensor update frequency)
- Default values and attribute keys

### Logging

All modules use `_LOGGER = logging.getLogger(__name__)` for consistent logging. Log connection attempts, state changes, and errors at appropriate levels.

### Entity Naming Convention

- `_attr_has_entity_name = True` enables friendly naming
- `_attr_name` sets display name (e.g., "Battery Level")
- `_attr_unique_id` uses pattern: `{entry_id}_{type}` (e.g., `abc123_battery`)

### Placeholder Implementations

**Current state**: Sensors return mock values (battery: 85%, temp: 35.5°C), switches toggle local state only, camera returns None.

**When implementing real SDK calls**:

Replace placeholder values using the Reachy Mini SDK:
```python
from reachy_mini import ReachyMini

async def async_update(self) -> None:
    """Fetch new state from robot."""
    try:
        # Connect to robot
        with ReachyMini(connection_mode="network") as mini:
            state = mini.state
            self._attr_native_value = state.get('battery_level')
            self._attr_available = True
    except Exception as err:
        _LOGGER.error("Error updating: %s", err)
        self._attr_available = False
```

Or use the REST API directly:
```python
import aiohttp

async def async_update(self) -> None:
    """Fetch via REST API."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://{self._host}:8000/api/state/full') as resp:
                state = await resp.json()
                self._attr_native_value = state.get('battery_level')
    except Exception as err:
        _LOGGER.error("Error: %s", err)
```

**Camera Streaming**: The Reachy Mini supports WebRTC, GStreamer, and OpenCV backends. Camera frames can be accessed via:
```python
with ReachyMini() as mini:
    frame = mini.media.get_frame()  # Returns numpy array (H, W, 3)
```

## Key Files Reference

- [\_\_init\_\_.py](custom_components/reachy_mini/__init__.py) - Integration setup, platform forwarding
- [sensor.py](custom_components/reachy_mini/sensor.py) - Connection/battery/temperature sensors
- [switch.py](custom_components/reachy_mini/switch.py) - Compliance/torque switches
- [camera.py](custom_components/reachy_mini/camera.py) - Teleop camera stream
- [config_flow.py](custom_components/reachy_mini/config_flow.py) - UI configuration
- [manifest.json](custom_components/reachy_mini/manifest.json) - Integration metadata

## Conventions

- **Async everywhere**: All entity methods use `async def` and `await` for I/O operations
- **Type hints**: All function signatures include type annotations
- **Broad exception handling**: Catch `Exception` in entity methods to prevent integration crashes, log errors
- **PEP 8 style**: Follow standard Python formatting conventions
