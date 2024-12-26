"""Support for EG4 Monitor sensors."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfElectricPotential,
    UnitOfFrequency,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN

@dataclass
class EG4SensorEntityDescription(SensorEntityDescription):
    """Class describing EG4 sensor entities."""
    value_fn: Callable[[dict[str, Any]], StateType] = None

SENSOR_TYPES: dict[str, EG4SensorEntityDescription] = {
    "battery_soc": EG4SensorEntityDescription(
        key="battery_soc",
        name="Battery State of Charge",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["Battery"]["SOC"],
    ),
    "battery_power": EG4SensorEntityDescription(
        key="battery_power",
        name="Battery Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["Battery"]["Power"],
    ),
    "battery_voltage": EG4SensorEntityDescription(
        key="battery_voltage",
        name="Battery Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["Battery"]["Voltage"],
    ),
    "solar_power": EG4SensorEntityDescription(
        key="solar_power",
        name="Solar Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["Solar"]["Total Power"],
    ),
    "pv1_power": EG4SensorEntityDescription(
        key="pv1_power",
        name="PV1 Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["Solar"]["PV1"]["Power"],
    ),
    "pv2_power": EG4SensorEntityDescription(
        key="pv2_power",
        name="PV2 Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["Solar"]["PV2"]["Power"],
    ),
    "grid_power": EG4SensorEntityDescription(
        key="grid_power",
        name="Grid Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["Grid"]["Power"],
    ),
    "grid_voltage": EG4SensorEntityDescription(
        key="grid_voltage",
        name="Grid Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["Grid"]["Voltage"],
    ),
    "grid_frequency": EG4SensorEntityDescription(
        key="grid_frequency",
        name="Grid Frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["Grid"]["Frequency"],
    ),
    "load_power": EG4SensorEntityDescription(
        key="load_power",
        name="Load Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["Load"]["Power"],
    ),
    "eps_power": EG4SensorEntityDescription(
        key="eps_power",
        name="EPS Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["EPS"]["Power"],
    ),
    "eps_frequency": EG4SensorEntityDescription(
        key="eps_frequency",
        name="EPS Frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["EPS"]["Frequency"],
    ),
    "today_solar": EG4SensorEntityDescription(
        key="today_solar",
        name="Today's Solar Generation",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data["Energy"]["Today"]["Solar Generation"],
    ),
    "today_grid_import": EG4SensorEntityDescription(
        key="today_grid_import",
        name="Today's Grid Import",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data["Energy"]["Today"]["Grid Import"],
    ),
    "today_grid_export": EG4SensorEntityDescription(
        key="today_grid_export",
        name="Today's Grid Export",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data["Energy"]["Today"]["Grid Export"],
    ),
    "total_solar": EG4SensorEntityDescription(
        key="total_solar",
        name="Total Solar Generation",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data["Energy"]["Total"]["Solar Generation"],
    ),
    "total_grid_import": EG4SensorEntityDescription(
        key="total_grid_import",
        name="Total Grid Import",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data["Energy"]["Total"]["Grid Import"],
    ),
    "total_grid_export": EG4SensorEntityDescription(
        key="total_grid_export",
        name="Total Grid Export",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data["Energy"]["Total"]["Grid Export"],
    ),
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up EG4 sensor based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    # Get enabled sensors from options
    enabled_sensors = {
        sensor_id: description
        for sensor_id, description in SENSOR_TYPES.items()
        if entry.options.get(sensor_id, True)  # Default to enabled if not in options
    }
    
    async_add_entities(
        EG4Sensor(coordinator, description)
        for description in enabled_sensors.values()
    )

class EG4Sensor(CoordinatorEntity, SensorEntity):
    """Representation of an EG4 sensor."""
    
    entity_description: EG4SensorEntityDescription
    
    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        description: EG4SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.data.get("serial_number", "unknown"))},
            "name": "EG4 Inverter",
            "manufacturer": "EG4 Electronics",
            "model": coordinator.data.get("model", "unknown"),
        }
        
    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        try:
            return self.entity_description.value_fn(self.coordinator.data)
        except (KeyError, TypeError):
            return None
            
    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and super().available
