# Configuration Guide

## Available Configuration Options

### Basic Configuration
The integration requires only your EG4 portal credentials:
- Username
- Password

### Advanced Options
You can customize the following settings:
- Update interval (default: 30 seconds)
- Sensor selection (choose which sensors to enable)

## Sensor Entities

### Battery Sensors
- **Battery State of Charge**
  - Entity ID: `sensor.eg4_battery_soc`
  - Unit: Percentage (%)
  - Description: Current battery charge level

- **Battery Power**
  - Entity ID: `sensor.eg4_battery_power`
  - Unit: Watts (W)
  - Description: Current battery power flow (positive = charging, negative = discharging)

### Solar Sensors
- **Solar Production**
  - Entity ID: `sensor.eg4_solar_production`
  - Unit: Watts (W)
  - Description: Current solar panel power production

- **Daily Solar Energy**
  - Entity ID: `sensor.eg4_daily_solar_energy`
  - Unit: Kilowatt-hours (kWh)
  - Description: Total solar energy produced today

### Grid Sensors
- **Grid Power**
  - Entity ID: `sensor.eg4_grid_power`
  - Unit: Watts (W)
  - Description: Current grid power flow (positive = importing, negative = exporting)

- **Grid Frequency**
  - Entity ID: `sensor.eg4_grid_frequency`
  - Unit: Hertz (Hz)
  - Description: Current grid frequency

## Lovelace Cards

### Example Battery Card
```yaml
type: entity
entity: sensor.eg4_battery_soc
name: Battery Level
```

### Example Power Flow Card
```yaml
type: custom:power-flow-card
entities:
  battery: sensor.eg4_battery_power
  solar: sensor.eg4_solar_production
  grid: sensor.eg4_grid_power
