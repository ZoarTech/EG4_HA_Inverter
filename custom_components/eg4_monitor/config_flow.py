"""Config flow for EG4 Monitor integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
import aiohttp

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .eg4_api import EG4API

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)

SENSOR_TYPES = {
    "battery_soc": "Battery State of Charge",
    "battery_power": "Battery Power",
    "battery_voltage": "Battery Voltage",
    "solar_power": "Solar Power",
    "pv1_power": "PV1 Power",
    "pv2_power": "PV2 Power",
    "grid_power": "Grid Power",
    "grid_voltage": "Grid Voltage",
    "grid_frequency": "Grid Frequency",
    "load_power": "Load Power",
    "eps_power": "EPS Power",
    "eps_frequency": "EPS Frequency",
    "today_solar": "Today's Solar Generation",
    "today_grid_import": "Today's Grid Import",
    "today_grid_export": "Today's Grid Export",
    "total_solar": "Total Solar Generation",
    "total_grid_import": "Total Grid Import",
    "total_grid_export": "Total Grid Export"
}

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    _LOGGER.debug("Starting validation of EG4 credentials")
    
    session = async_get_clientsession(hass)
    
    try:
        api = EG4API(
            username=data[CONF_USERNAME],
            password=data[CONF_PASSWORD],
            session=session,
        )
        
        _LOGGER.debug("Attempting to login to EG4")
        login_result = await api.login()
        
        if not login_result:
            _LOGGER.error("Login failed with invalid credentials")
            raise InvalidAuth
            
        _LOGGER.debug("Login successful, attempting to get system data")
        system_data = await api.get_system_data()
        
        if not system_data:
            _LOGGER.error("Could not retrieve system data after successful login")
            raise CannotConnect
            
        _LOGGER.debug("Successfully retrieved system data")
        return {"title": f"EG4 Monitor ({data[CONF_USERNAME]})"}
        
    except aiohttp.ClientError as err:
        _LOGGER.error("Connection error occurred: %s", err)
        raise CannotConnect from err
    except Exception as err:
        _LOGGER.exception("Unexpected error occurred during validation: %s", err)
        raise CannotConnect from err
    finally:
        if 'api' in locals():
            await api.close()

class SensorSelectFlow(config_entries.OptionsFlow):
    """Handle sensor selection options."""
    
    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
        
    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle sensor selection."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
            
        options = {}
        for sensor_id, description in SENSOR_TYPES.items():
            options[
                vol.Optional(
                    sensor_id,
                    default=self.config_entry.options.get(sensor_id, True),
                    description=description,
                )
            ] = bool
            
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(options),
            description_placeholders={
                "sensor_descriptions": "\n".join(
                    f"- {description}" for description in SENSOR_TYPES.values()
                )
            },
        )

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EG4 Monitor."""
    
    VERSION = 1
    
    @staticmethod
    @config_entries.HANDLERS.register(DOMAIN)
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return SensorSelectFlow(config_entry)
        
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Initialize all sensors as enabled by default
                options = {sensor_id: True for sensor_id in SENSOR_TYPES}
                
                return self.async_create_entry(
                    title=info["title"],
                    data=user_input,
                    options=options,
                )
                
        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
