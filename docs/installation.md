# Installation Guide

## Prerequisites
- Home Assistant version 2023.8.0 or newer
- Access to your Home Assistant configuration directory
- Valid EG4 portal account credentials

## Installation Methods

### Method 1: HACS (Recommended)

Since this is a custom integration, you'll need to add it as a custom repository in HACS:

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots menu (⋮) in the top right corner
4. Select "Custom repositories"
5. Enter the repository URL: `https://github.com/ZoarTech/EG4_HA_Inverter`
6. Select "Integration" as the category
7. Click "Add"
8. Close the custom repositories dialog
9. Click the "+ Explore & Download Repositories" button
10. Search for "EG4 Monitor"
11. Click on it and then click "Download"
12. Restart Home Assistant

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

## Updating

### Via HACS
1. Open HACS > Integrations
2. Find "EG4 Monitor" in your installed integrations
3. Click on it
4. If an update is available, click "Update"
5. Restart Home Assistant

### Manual Update
1. Download the latest release
2. Replace the existing `custom_components/eg4_monitor` directory
3. Restart Home Assistant

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
1. Confirm the files are in the correct location (`custom_components/eg4_monitor/`)
2. Check that `manifest.json` exists in the integration folder
3. Clear your browser cache
4. Restart Home Assistant

#### HACS Can't Find the Integration
1. Make sure you added it as a custom repository first (see Method 1 above)
2. Try refreshing HACS (three dots menu > "Reload window")
3. Check that the repository URL is correct

## Support

If you encounter any issues:
1. Check the [FAQ](faq.md)
2. Search existing [GitHub Issues](https://github.com/ZoarTech/EG4_HA_Inverter/issues)
3. Create a new issue with detailed information about your problem
