"""Support for Reachy Mini sensors."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Reachy Mini sensors from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    host = data["host"]
    port = data["port"]
    
    sensors = [
        ReachyMiniConnectionSensor(entry, host, port),
        ReachyMiniBatterySensor(entry, host, port),
        ReachyMiniTemperatureSensor(entry, host, port),
    ]
    
    async_add_entities(sensors)


class ReachyMiniSensorBase(SensorEntity):
    """Base class for Reachy Mini sensors."""

    def __init__(self, entry: ConfigEntry, host: str, port: int) -> None:
        """Initialize the sensor."""
        self._entry = entry
        self._host = host
        self._port = port
        self._attr_has_entity_name = True

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this Reachy Mini."""
        return DeviceInfo(
            identifiers={(DOMAIN, f"{self._host}:{self._port}")},
            name=f"Reachy Mini ({self._host})",
            manufacturer="Pollen Robotics",
            model="Reachy Mini",
            sw_version="1.0",
        )


class ReachyMiniConnectionSensor(ReachyMiniSensorBase):
    """Representation of Reachy Mini connection status sensor."""

    def __init__(self, entry: ConfigEntry, host: str, port: int) -> None:
        """Initialize the connection sensor."""
        super().__init__(entry, host, port)
        self._attr_name = "Connection Status"
        self._attr_unique_id = f"{entry.entry_id}_connection"
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = ["connected", "disconnected"]
        self._attr_native_value = "disconnected"

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            # In a real implementation, you would check the actual connection
            # For now, we'll simulate it
            self._attr_native_value = "connected"
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error updating connection status: %s", err)
            self._attr_native_value = "disconnected"


class ReachyMiniBatterySensor(ReachyMiniSensorBase):
    """Representation of Reachy Mini battery level sensor."""

    def __init__(self, entry: ConfigEntry, host: str, port: int) -> None:
        """Initialize the battery sensor."""
        super().__init__(entry, host, port)
        self._attr_name = "Battery Level"
        self._attr_unique_id = f"{entry.entry_id}_battery"
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_state_class = SensorStateClass.MEASUREMENT

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            # In a real implementation, you would get the actual battery level
            # from the Reachy Mini SDK: battery = reachy.battery_level
            # Placeholder value for testing purposes
            self._attr_native_value = 85
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error updating battery level: %s", err)
            self._attr_native_value = None


class ReachyMiniTemperatureSensor(ReachyMiniSensorBase):
    """Representation of Reachy Mini temperature sensor."""

    def __init__(self, entry: ConfigEntry, host: str, port: int) -> None:
        """Initialize the temperature sensor."""
        super().__init__(entry, host, port)
        self._attr_name = "Temperature"
        self._attr_unique_id = f"{entry.entry_id}_temperature"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_state_class = SensorStateClass.MEASUREMENT

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            # In a real implementation, you would get the actual temperature
            # from the Reachy Mini SDK: temperature = reachy.temperature
            # Placeholder value for testing purposes (typical operating temp)
            self._attr_native_value = 35.5
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error updating temperature: %s", err)
            self._attr_native_value = None
