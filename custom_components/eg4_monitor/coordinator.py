"""DataUpdateCoordinator for the EG4 Monitor integration."""
from datetime import timedelta
import logging
from typing import Any

import aiohttp
import async_timeout
from bs4 import BeautifulSoup

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGIN_URL, MONITOR_URL, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

class EG4UpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the EG4 portal."""

    def __init__(
        self, hass: HomeAssistant, session: aiohttp.ClientSession, username: str, password: str
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.session = session
        self.username = username
        self.password = password
        self._cookies = {}

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            async with async_timeout.timeout(30):
                # Login if needed
                if not self._cookies:
                    await self._login()
                
                # Fetch the monitor page
                async with self.session.get(MONITOR_URL, cookies=self._cookies) as response:
                    response.raise_for_status()
                    html = await response.text()
                    
                # Parse the data
                return self._parse_monitor_page(html)
                
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    async def _login(self) -> None:
        """Log in to EG4 portal."""
        try:
            # First get the login page to get any required tokens/cookies
            async with self.session.get(LOGIN_URL) as response:
                response.raise_for_status()
                
            # Now perform login
            data = {
                "username": self.username,
                "password": self.password,
            }
            async with self.session.post(LOGIN_URL, data=data) as response:
                response.raise_for_status()
                self._cookies = response.cookies
                
        except Exception as err:
            raise UpdateFailed(f"Failed to log in: {err}")

    def _parse_monitor_page(self, html: str) -> dict[str, Any]:
        """Parse the monitor page HTML to extract relevant data."""
        soup = BeautifulSoup(html, 'html.parser')
        data = {}
        
        # TODO: Extract relevant data from the page
        # Example:
        # data['battery_soc'] = float(soup.find('div', {'id': 'battery-soc'}).text.strip('%'))
        
        return data
