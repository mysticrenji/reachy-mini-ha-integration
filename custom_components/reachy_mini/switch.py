"""Support for Reachy Mini switches."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
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
    """Set up Reachy Mini switches from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    host = data["host"]
    port = data["port"]
    
    switches = [
        ReachyMiniComplianceSwitch(entry, host, port),
        ReachyMiniTorqueSwitch(entry, host, port),
    ]
    
    async_add_entities(switches)


class ReachyMiniSwitchBase(SwitchEntity):
    """Base class for Reachy Mini switches."""

    def __init__(self, entry: ConfigEntry, host: str, port: int) -> None:
        """Initialize the switch."""
        self._entry = entry
        self._host = host
        self._port = port
        self._attr_has_entity_name = True
        self._is_on = False

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

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._is_on


class ReachyMiniComplianceSwitch(ReachyMiniSwitchBase):
    """Representation of Reachy Mini compliance mode switch."""

    def __init__(self, entry: ConfigEntry, host: str, port: int) -> None:
        """Initialize the compliance switch."""
        super().__init__(entry, host, port)
        self._attr_name = "Compliance Mode"
        self._attr_unique_id = f"{entry.entry_id}_compliance"
        self._attr_icon = "mdi:robot"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        try:
            # In a real implementation, you would enable compliance mode
            # using the Reachy Mini SDK
            _LOGGER.info("Enabling compliance mode for Reachy Mini")
            self._is_on = True
            self.async_write_ha_state()
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error enabling compliance mode: %s", err)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        try:
            # In a real implementation, you would disable compliance mode
            # using the Reachy Mini SDK
            _LOGGER.info("Disabling compliance mode for Reachy Mini")
            self._is_on = False
            self.async_write_ha_state()
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error disabling compliance mode: %s", err)


class ReachyMiniTorqueSwitch(ReachyMiniSwitchBase):
    """Representation of Reachy Mini torque switch."""

    def __init__(self, entry: ConfigEntry, host: str, port: int) -> None:
        """Initialize the torque switch."""
        super().__init__(entry, host, port)
        self._attr_name = "Torque"
        self._attr_unique_id = f"{entry.entry_id}_torque"
        self._attr_icon = "mdi:engine"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        try:
            # In a real implementation, you would enable torque
            # using the Reachy Mini SDK
            _LOGGER.info("Enabling torque for Reachy Mini")
            self._is_on = True
            self.async_write_ha_state()
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error enabling torque: %s", err)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        try:
            # In a real implementation, you would disable torque
            # using the Reachy Mini SDK
            _LOGGER.info("Disabling torque for Reachy Mini")
            self._is_on = False
            self.async_write_ha_state()
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error disabling torque: %s", err)
