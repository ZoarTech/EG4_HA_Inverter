"""EG4 Electronics API Module."""
import asyncio
import json
import logging
import re
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import aiohttp

_LOGGER = logging.getLogger(__name__)

class EG4API:
    """API Client for EG4 Electronics."""
    
    def __init__(
        self,
        username: str,
        password: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize the API client."""
        self.username = username
        self.password = password
        self.session = session
        self.base_url = "https://monitor.eg4electronics.com/WManage"
        self.logged_in = False
        self.serial_number = None
        
    async def login(self) -> bool:
        """Login to EG4 portal."""
        try:
            login_url = f"{self.base_url}/web/login"
            _LOGGER.debug("Attempting to login at URL: %s", login_url)
            
            # Get CSRF token
            async with self.session.get(login_url) as response:
                if response.status != 200:
                    _LOGGER.error("Failed to access login page. Status: %s", response.status)
                    response_text = await response.text()
                    _LOGGER.debug("Response: %s", response_text)
                    return False
                    
                html = await response.text()
                _LOGGER.debug("Successfully accessed login page")
                
            # Login request
            login_data = {
                "account": self.username,  
                "password": self.password,
                "remember": "false",
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            encoded_data = urlencode(login_data)
            _LOGGER.debug("Sending login request")
            async with self.session.post(login_url, data=encoded_data, headers=headers) as response:
                if response.status != 200:
                    _LOGGER.error("Login failed with status: %s", response.status)
                    response_text = await response.text()
                    _LOGGER.debug("Response: %s", response_text)
                    return False
                
                response_text = await response.text()
                _LOGGER.debug("Login response: %s", response_text)
                
                # Check if login was successful by looking for specific patterns
                if "Invalid username or password" in response_text or "Invalid account or password" in response_text:
                    _LOGGER.error("Login failed: Invalid credentials")
                    return False
                    
                if "Login successful" in response_text or "Welcome" in response_text or "success" in response_text.lower():
                    _LOGGER.debug("Login successful")
                    self.logged_in = True
                    return True
                    
                _LOGGER.error("Login failed: Unexpected response")
                return False
                
        except aiohttp.ClientError as err:
            _LOGGER.error("Network error during login: %s", err)
            return False
        except Exception as err:
            _LOGGER.exception("Unexpected error during login: %s", err)
            return False
            
    async def get_system_data(self) -> Dict[str, Any]:
        """Get current system data."""
        if not self.logged_in:
            _LOGGER.debug("Not logged in, attempting login")
            if not await self.login():
                _LOGGER.error("Failed to login during system data request")
                return None
                
        try:
            # Get cookies and headers
            cookies_dict = {}
            for cookie in self.session.cookie_jar:
                cookies_dict[cookie.key] = cookie.value
                
            cookies_str = '; '.join([f"{k}={v}" for k, v in cookies_dict.items()])
            
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': cookies_str,
                'Origin': 'https://monitor.eg4electronics.com',
                'Referer': 'https://monitor.eg4electronics.com/WManage/web/monitor/inverter',
                'User-Agent': 'Mozilla/5.0',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            # Get serial number if not already obtained
            if not self.serial_number:
                _LOGGER.debug("Fetching serial number")
                monitor_url = f"{self.base_url}/web/monitor/inverter"
                async with self.session.get(monitor_url) as response:
                    if response.status == 200:
                        html = await response.text()
                        _LOGGER.debug("Got monitor page, searching for serial number")
                        
                        # Try multiple patterns for serial number
                        patterns = [
                            r'serialNum["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                            r'serialNumber["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                            r'sn["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                            r'deviceSn["\']?\s*[:=]\s*["\']([^"\']+)["\']'
                        ]
                        
                        for pattern in patterns:
                            sn_matches = re.findall(pattern, html, re.IGNORECASE)
                            if sn_matches:
                                self.serial_number = sn_matches[0]
                                _LOGGER.debug("Found serial number using pattern %s: %s", pattern, self.serial_number)
                                break
                                
                        if not self.serial_number:
                            _LOGGER.debug("Serial number not found in HTML, trying device list")
                            # Try to get the serial number from the device list
                            list_url = f"{self.base_url}/api/inverter/getInverterList"
                            _LOGGER.debug("Fetching device list from: %s", list_url)
                            
                            async with self.session.post(
                                list_url,
                                headers=headers,
                                data=urlencode({})  # Empty data as it might just need the session cookie
                            ) as list_response:
                                _LOGGER.debug("Device list response status: %s", list_response.status)
                                if list_response.status == 200:
                                    try:
                                        data = await list_response.json()
                                        _LOGGER.debug("Device list response: %s", data)
                                        
                                        if data.get('success') and data.get('rows'):
                                            self.serial_number = data['rows'][0].get('serialNum')
                                            _LOGGER.debug("Found serial number from device list: %s", self.serial_number)
                                        else:
                                            _LOGGER.debug("No devices found in the list response")
                                            
                                            # Try alternate API endpoint
                                            alt_url = f"{self.base_url}/api/device/list"
                                            _LOGGER.debug("Trying alternate device list endpoint: %s", alt_url)
                                            
                                            async with self.session.post(
                                                alt_url,
                                                headers=headers,
                                                data=urlencode({})
                                            ) as alt_response:
                                                if alt_response.status == 200:
                                                    try:
                                                        alt_data = await alt_response.json()
                                                        _LOGGER.debug("Alternate device list response: %s", alt_data)
                                                        
                                                        if alt_data.get('success') and alt_data.get('data'):
                                                            devices = alt_data['data']
                                                            if isinstance(devices, list) and devices:
                                                                self.serial_number = devices[0].get('sn') or devices[0].get('serialNum')
                                                                _LOGGER.debug("Found serial number from alternate endpoint: %s", self.serial_number)
                                                    except Exception as err:
                                                        _LOGGER.error("Error parsing alternate device list response: %s", err)
                                                        
                                    except Exception as err:
                                        _LOGGER.error("Error parsing device list response: %s", err)
                                        
            if not self.serial_number:
                _LOGGER.error("Could not find serial number after trying all methods")
                return None
                
            # Get runtime data
            _LOGGER.debug("Fetching runtime data")
            system_data = {}
            async with self.session.post(
                f"{self.base_url}/api/inverter/getInverterRuntime",
                headers=headers,
                data=urlencode({"serialNum": self.serial_number})
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('success'):
                        _LOGGER.debug("Raw grid frequency value: %s", data.get('fgrid'))
                        
                        system_data = {
                            "Time": data.get('deviceTime', 'Unknown'),
                            "Status": data.get('statusText', 'Unknown'),
                            "Battery": {
                                "SOC": float(data.get('soc', 0)),
                                "Power": float(data.get('batPower', 0)),
                                "Voltage": float(data.get('vBat', 0)) / 10,
                                "Current": float(data.get('iBat', 0)) / 10 if 'iBat' in data else None,
                                "Temperature": float(data.get('batTemp', 0)) if 'batTemp' in data else None
                            },
                            "Solar": {
                                "PV1": {
                                    "Voltage": float(data.get('vpv1', 0)) / 10,
                                    "Current": float(data.get('ipv1', 0)) / 10,
                                    "Power": float(data.get('ppv1', 0))
                                },
                                "PV2": {
                                    "Voltage": float(data.get('vpv2', 0)) / 10,
                                    "Current": float(data.get('ipv2', 0)) / 10,
                                    "Power": float(data.get('ppv2', 0))
                                },
                                "Total Power": float(data.get('ppv', 0))
                            },
                            "Grid": {
                                "Voltage": float(data.get('vgrid', 0)) / 10,
                                "Frequency": float(data.get('fgrid', 0)) / 100 if data.get('fgrid') else None,
                                "Power": float(data.get('pgrid', 0)),  # Positive = import, Negative = export
                                "Current": float(data.get('igrid', 0)) / 10
                            },
                            "Load": {
                                "Power": float(data.get('pload', 0)),
                                "Current": float(data.get('iload', 0)) / 10 if 'iload' in data else None
                            },
                            "EPS": {
                                "Voltage": float(data.get('veps', 0)) / 10 if 'veps' in data else None,
                                "Frequency": float(data.get('feps', 0)) / 100 if 'feps' in data else None,
                                "Power": float(data.get('peps', 0)) if 'peps' in data else None
                            },
                            "Temperature": {
                                "Inverter": float(data.get('temp', 0)) if 'temp' in data else None,
                                "Environment": float(data.get('envTemp', 0)) if 'envTemp' in data else None
                            }
                        }
                        
            # Get energy statistics
            _LOGGER.debug("Fetching energy statistics")
            async with self.session.post(
                f"{self.base_url}/api/inverter/getInverterEnergy",
                headers=headers,
                data=urlencode({"serialNum": self.serial_number})
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('success'):
                        system_data["Energy"] = {
                            "Today": {
                                "Solar Generation": float(data.get('eToday', 0)) / 10,  # kWh
                                "Grid Import": float(data.get('eToGridToday', 0)) / 10,  # kWh
                                "Grid Export": float(data.get('eToUserToday', 0)) / 10,  # kWh
                                "Battery Charge": float(data.get('eChargeToday', 0)) / 10,  # kWh
                                "Battery Discharge": float(data.get('eDischargeToday', 0)) / 10  # kWh
                            },
                            "Total": {
                                "Solar Generation": float(data.get('eTotal', 0)) / 10,  # kWh
                                "Grid Import": float(data.get('eToGridTotal', 0)) / 10,  # kWh
                                "Grid Export": float(data.get('eToUserTotal', 0)) / 10,  # kWh
                                "Battery Charge": float(data.get('eChargeTotal', 0)) / 10,  # kWh
                                "Battery Discharge": float(data.get('eDischargeTotal', 0)) / 10  # kWh
                            }
                        }
                        
            return system_data
            
        except aiohttp.ClientError as err:
            _LOGGER.error("Network error getting system data: %s", err)
            return None
        except Exception as err:
            _LOGGER.exception("Unexpected error getting system data: %s", err)
            return None
            
    async def close(self) -> None:
        """Close the session."""
        # Don't close the session as it's managed by Home Assistant
        self.logged_in = False
        self.serial_number = None
        
    async def __aenter__(self):
        """Async enter."""
        return self
        
    async def __aexit__(self, *exc_info):
        """Async exit."""
        await self.close()
