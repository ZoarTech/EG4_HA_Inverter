# Home Assistant EG4 Monitor Integration

![EG4 Monitor Banner](docs/images/banner.png)

This is a custom Home Assistant integration for monitoring EG4 inverter systems. It connects to the EG4 web portal to fetch real-time data about your solar system.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/ZoarTech/EG4_HA_Inverter.svg)](https://GitHub.com/ZoarTech/EG4_HA_Inverter/releases/)

## Features

- Real-time monitoring of your EG4 inverter system
- Battery State of Charge monitoring
- Solar production monitoring
- Grid import/export monitoring
- Battery charge/discharge monitoring
- Customizable update intervals
- User-friendly sensor names and icons

![Dashboard Example](docs/images/dashboard.png)

## Quick Start

1. Copy the `custom_components/eg4_monitor` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant
3. Add the integration through the Home Assistant UI

For detailed instructions, see our [Installation Guide](docs/installation.md).

## Documentation

- [Installation Guide](docs/installation.md)
- [Configuration Guide](docs/configuration.md)
- [FAQ](docs/faq.md)

## Screenshots

### Configuration
![Configuration](docs/images/config.png)

### Energy Dashboard
![Energy Dashboard](docs/images/energy.png)

### Battery Status
![Battery Status](docs/images/battery.png)

## Configuration

The integration requires your EG4 portal credentials:
- Username
- Password

For detailed configuration options, see our [Configuration Guide](docs/configuration.md).

## Available Sensors

| Sensor | Unit | Description |
|--------|------|-------------|
| Battery State of Charge | % | Current battery charge level |
| Solar Production | W | Current solar panel power production |
| Grid Power | W | Current grid power flow |
| Battery Power | W | Current battery power flow |
| Daily Energy Production | kWh | Total solar energy produced today |
| Daily Grid Import/Export | kWh | Net grid energy exchange |
| Daily Battery Charge/Discharge | kWh | Net battery energy exchange |

## Support

- Check our [FAQ](docs/faq.md)
- Report issues on [GitHub](https://github.com/ZoarTech/EG4_HA_Inverter/issues)
- Join our [Discord community](#) (coming soon)

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This integration is not officially associated with EG4 Electronics. Use at your own risk.