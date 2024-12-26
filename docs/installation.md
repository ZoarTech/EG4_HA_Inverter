# Installation Guide

## Prerequisites
- Home Assistant version 2023.8.0 or newer
- Access to your Home Assistant configuration directory
- Valid EG4 portal account credentials

## Installation Methods

### Method 1: HACS (Recommended)
1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the "+" button
4. Search for "EG4 Monitor"
5. Click "Install"
6. Restart Home Assistant

### Method 2: Manual Installation
1. Download the latest release from the [releases page](https://github.com/ZoarTech/EG4_HA_Inverter/releases)
2. Extract the `custom_components/eg4_monitor` directory
3. Copy it to your Home Assistant's `custom_components` directory
4. Restart Home Assistant

## Configuration

1. Go to Home Assistant's Configuration > Integrations
2. Click the "+ Add Integration" button
3. Search for "EG4 Monitor"
4. Enter your EG4 portal credentials:
   - Username
   - Password
5. Click "Submit"

## Troubleshooting

### Common Issues

#### Cannot Connect Error
If you receive a "Cannot Connect" error:
1. Verify your EG4 portal credentials
2. Check your internet connection
3. Ensure the EG4 portal is accessible
4. Check Home Assistant logs for detailed error messages

#### Integration Not Found
If "EG4 Monitor" doesn't appear in the integrations list:
1. Confirm the files are in the correct location
2. Clear your browser cache
3. Restart Home Assistant

## Support

If you encounter any issues:
1. Check the [FAQ](faq.md)
2. Search existing [GitHub Issues](https://github.com/ZoarTech/EG4_HA_Inverter/issues)
3. Create a new issue with detailed information about your problem
