"""Config flow for OpenEVSE PV Load Manager integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow

from .const import CONF_NUM_STATIONS, DOMAIN


class OpenEVSEPVLoadManagerConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OpenEVSE PV Load Manager."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Prevent duplicate entries
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="OpenEVSE PV Load Manager",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NUM_STATIONS, default=3): vol.All(
                        vol.Coerce(int), vol.Range(min=1, max=3)
                    ),
                }
            ),
        )
