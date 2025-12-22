"""Config flow for Reachy Mini integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, DEFAULT_PORT

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    }
)


class ReachyMiniConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Reachy Mini."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input.get(CONF_PORT, DEFAULT_PORT)
            
            # Set unique ID to prevent duplicate entries
            await self.async_set_unique_id(f"{host}:{port}")
            self._abort_if_unique_id_configured()

            # Validate the connection
            try:
                # Try to import and test connection
                # For now, we'll assume the connection is valid
                # In a production environment, you would test the actual connection here
                _LOGGER.info("Setting up Reachy Mini at %s:%s", host, port)
                
                return self.async_create_entry(
                    title=f"Reachy Mini ({host})",
                    data={
                        CONF_HOST: host,
                        CONF_PORT: port,
                    },
                )
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.error("Error connecting to Reachy Mini: %s", err)
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
