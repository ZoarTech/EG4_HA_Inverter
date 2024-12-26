"""Constants for the EG4 Monitor integration."""

DOMAIN = "eg4_monitor"

# Base URLs
BASE_URL = "https://monitor.eg4electronics.com/WManage"
LOGIN_URL = f"{BASE_URL}/web/login"
MONITOR_URL = f"{BASE_URL}/web/monitor/inverter"

# Update interval in seconds (5 minutes)
UPDATE_INTERVAL = 300
