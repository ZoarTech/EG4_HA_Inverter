"""The EG4 Monitor integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_SCAN_INTERVAL,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN
from .eg4_api import EG4API

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]
DEFAULT_SCAN_INTERVAL = 30

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the EG4 Monitor component."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up EG4 Monitor from a config entry."""
    _LOGGER.debug("Setting up EG4 Monitor integration")
    
    session = async_get_clientsession(hass)
    
    api = EG4API(
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        session=session,
    )
    
    try:
        _LOGGER.debug("Attempting to login to EG4")
        if not await api.login():
            _LOGGER.error("Failed to login to EG4")
            return False
            
        _LOGGER.debug("Login successful")
    except Exception as err:
        _LOGGER.error("Error logging in to EG4: %s", err)
        return False
        
    async def async_update_data():
        """Fetch data from API."""
        try:
            _LOGGER.debug("Fetching updated data from EG4")
            data = await api.get_system_data()
            if not data:
                raise UpdateFailed("No data received from EG4")
            _LOGGER.debug("Successfully received data from EG4")
            return data
        except Exception as err:
            _LOGGER.error("Error communicating with EG4 API: %s", err)
            raise UpdateFailed(f"Error communicating with API: {err}")
            
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)),
    )
    
    # Fetch initial data
    _LOGGER.debug("Performing initial data refresh")
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "api": api,
    }
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Unloading EG4 Monitor integration")
    
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        api = hass.data[DOMAIN][entry.entry_id]["api"]
        await api.close()  # This now just resets state, doesn't close session
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.debug("Successfully unloaded EG4 Monitor integration")
        
    return unload_ok
