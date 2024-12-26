# Frequently Asked Questions (FAQ)

## General Questions

### What is the EG4 Monitor integration?
The EG4 Monitor integration allows you to monitor your EG4 inverter system through Home Assistant. It provides real-time data about your solar production, battery status, and grid usage.

### Which EG4 models are supported?
The integration works with any EG4 inverter system that can be monitored through the EG4 web portal.

### How often is the data updated?
By default, the data is updated every 30 seconds. This interval can be adjusted in the configuration.

## Installation Questions

### Why can't I find the integration in HACS?
The integration needs to be submitted and approved for HACS. We're working on this process.

### Do I need to keep the EG4 portal credentials?
Yes, the integration needs your credentials to fetch data from the EG4 portal.

## Troubleshooting

### Why am I seeing "Cannot Connect" errors?
This usually happens when:
1. Your credentials are incorrect
2. The EG4 portal is temporarily unavailable
3. Your internet connection is unstable

### Why are some sensors showing "Unknown"?
This can happen when:
1. The specific data point is not available from your inverter
2. There's a temporary communication issue
3. The sensor is not supported by your model

### How can I debug connection issues?
1. Enable debug logging for the integration
2. Check the Home Assistant logs
3. Verify your network connection
4. Test if you can log in to the EG4 portal directly

## Feature Requests and Support

### How can I request a new feature?
Please create a new issue on our [GitHub repository](https://github.com/ZoarTech/EG4_HA_Inverter/issues) with the "feature request" label.

### Where can I get support?
1. Check this FAQ
2. Search existing [GitHub Issues](https://github.com/ZoarTech/EG4_HA_Inverter/issues)
3. Create a new issue
4. Join our [Discord community](#) (coming soon)
