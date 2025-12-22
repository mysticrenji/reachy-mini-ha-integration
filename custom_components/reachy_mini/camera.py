"""Support for Reachy Mini cameras."""
from __future__ import annotations

import logging

from homeassistant.components.camera import Camera, CameraEntityFeature
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
    """Set up Reachy Mini cameras from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    host = data["host"]
    port = data["port"]
    
    cameras = [
        ReachyMiniCamera(entry, host, port, "teleop"),
    ]
    
    async_add_entities(cameras)


class ReachyMiniCamera(Camera):
    """Representation of a Reachy Mini camera."""

    def __init__(self, entry: ConfigEntry, host: str, port: int, camera_name: str) -> None:
        """Initialize the camera."""
        super().__init__()
        self._entry = entry
        self._host = host
        self._port = port
        self._camera_name = camera_name
        self._attr_has_entity_name = True
        self._attr_name = f"{camera_name.title()} Camera"
        self._attr_unique_id = f"{entry.entry_id}_{camera_name}_camera"
        self._attr_brand = "Pollen Robotics"
        self._attr_model = "Reachy Mini"
        self._is_streaming = False

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
    def is_streaming(self) -> bool:
        """Return true if the camera is streaming."""
        return self._is_streaming

    @property
    def supported_features(self) -> CameraEntityFeature:
        """Return supported features."""
        return CameraEntityFeature.STREAM

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image from the camera."""
        try:
            # In a real implementation, you would get the image from the Reachy Mini SDK
            # Example: return await self.hass.async_add_executor_job(
            #     self._get_camera_frame
            # )
            # For now, return None as this requires actual SDK integration
            _LOGGER.debug("Fetching camera image for %s", self._camera_name)
            return None
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error fetching camera image: %s", err)
            return None

    async def stream_source(self) -> str | None:
        """Return the stream source URL."""
        # In a real implementation, this would return the RTSP or HTTP stream URL
        # from the Reachy Mini robot, for example:
        # return f"http://{self._host}:{self._port}/video_feed"
        # or using the SDK to get the stream endpoint
        _LOGGER.info("Stream source requested for %s camera", self._camera_name)
        return None

    async def async_turn_on(self) -> None:
        """Turn on the camera stream."""
        try:
            # In a real implementation, you would start the camera stream
            # using the Reachy Mini SDK
            _LOGGER.info("Turning on camera stream for %s", self._camera_name)
            self._is_streaming = True
            self.async_write_ha_state()
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error turning on camera: %s", err)
            self._is_streaming = False
            self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        """Turn off the camera stream."""
        try:
            # In a real implementation, you would stop the camera stream
            # using the Reachy Mini SDK
            _LOGGER.info("Turning off camera stream for %s", self._camera_name)
            self._is_streaming = False
            self.async_write_ha_state()
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error turning off camera: %s", err)
            self._is_streaming = False
            self.async_write_ha_state()
