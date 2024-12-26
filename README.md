# Home Assistant EG4 Monitor Integration

This is a custom Home Assistant integration for monitoring EG4 inverter systems. It connects to the EG4 web portal to fetch real-time data about your solar system.

## Installation

1. Copy the `custom_components/eg4_monitor` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant
3. Go to Configuration > Integrations
4. Click the "+ Add Integration" button
5. Search for "EG4 Monitor"
6. Enter your EG4 portal credentials

## Features

- Battery State of Charge monitoring
- Solar production monitoring
- Grid import/export monitoring
- Battery charge/discharge monitoring

## Configuration

The integration requires your EG4 portal credentials:
- Username
- Password

## Sensors

The integration provides the following sensors:
- Battery State of Charge (%)
- Solar Production (W)
- Grid Power (W)
- Battery Power (W)
- Daily Energy Production (kWh)
- Daily Grid Import/Export (kWh)
- Daily Battery Charge/Discharge (kWh)

## Development

This integration is under development. Feel free to contribute by submitting issues or pull requests.

## Disclaimer

This integration is not officially associated with EG4 Electronics. Use at your own risk.