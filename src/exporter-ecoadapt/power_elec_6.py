from enum import Enum

from power_elec_6_settings import PE6_MEASUREMENTS_DEFINITION
from pydantic import BaseModel, PositiveInt


class InvalidMeasurementException(Exception):
    "Raised when Measurement does not exist."
    pass


class InvalidConnectorException(Exception):
    "Raised when Measurement does not exist."
    pass


class Measurement(BaseModel):
    name: str
    unit: str
    wpc: PositiveInt
    registers_start: PositiveInt
    registers_end: PositiveInt

    def register_number(self, *, connector: int, channel: int, connectors: int = 6, channels: int = 3):
        """The function for obtaining the register number for connector n channel m"""

        if connector not in range(1, connectors + 1):
            raise InvalidConnectorException(f"invalid {connector} for Power-Elec-6")

        if channel not in range(1, channels + 1):
            raise InvalidConnectorException(f"invalid {channel} for Power-Elec-6")

        return self.registers_start + ((connector - 1) * 3 + channel - 1) * self.wpc


class CircuitConfiguration(Enum):
    DISABLED = 0x0000
    SINGLE_PHASE = 0x0001
    THREE_PHASE_WITH_NEUTRAL = 0x0002
    BALANCED_THREE_PHASE_WITH_NEUTRAL = 0x0003
    THREE_PHASE_WITHOUT_NEUTRAL = 0x0004
    BALANCED_THREE_PHASE_NO_NEUTRAL = 0x0005
    THREE_PHASE_WITH_VOLTAGE_TRANSFORMER = 0x0006


def _get_measurement_definition(measurement: str, measurements_definition: dict) -> dict:

    if measurement not in measurements_definition:
        raise InvalidMeasurementException(f"{measurement} is not a valid measurement for Power-Elec-6")

    return measurements_definition[measurement]


class POWER_ELEC_6():

    def __init__(self):
        self.active_energy_import_index = Measurement(
            **_get_measurement_definition('active_energy_import_index', PE6_MEASUREMENTS_DEFINITION))
        self.reactive_energy_import_index = Measurement(
            **_get_measurement_definition('reactive_energy_import_index', PE6_MEASUREMENTS_DEFINITION))
        self.active_energy_export_index = Measurement(
            **_get_measurement_definition('active_energy_export_index', PE6_MEASUREMENTS_DEFINITION))
        self.reactive_energy_export_index = Measurement(
            **_get_measurement_definition('reactive_energy_export_index', PE6_MEASUREMENTS_DEFINITION))
        self.active_power = Measurement(**_get_measurement_definition('active_power', PE6_MEASUREMENTS_DEFINITION))
        self.reactive_power = Measurement(**_get_measurement_definition('reactive_power', PE6_MEASUREMENTS_DEFINITION))
        self.power_factor = Measurement(**_get_measurement_definition('power_factor', PE6_MEASUREMENTS_DEFINITION))
        self.rms_current = Measurement(**_get_measurement_definition('rms_current', PE6_MEASUREMENTS_DEFINITION))
        self.rms_current_1_min_average = Measurement(
            **_get_measurement_definition('rms_current_1_min_average', PE6_MEASUREMENTS_DEFINITION))
        self.rms_voltage = Measurement(**_get_measurement_definition('rms_voltage', PE6_MEASUREMENTS_DEFINITION))
        self.rms_voltage_1_min_average = Measurement(
            **_get_measurement_definition('rms_voltage_1_min_average', PE6_MEASUREMENTS_DEFINITION))
        self.frequency = Measurement(**_get_measurement_definition('frequency', PE6_MEASUREMENTS_DEFINITION))


if __name__ == "__main__":
    # POWER_ELEC_6_MEASUREMENTS = {
    #     measurement_namne: Measurement(**measurement)
    #     for measurement_namne, measurement in power_elec_6_measurements_definition.items()
    # }
    pe6 = POWER_ELEC_6()
    print(pe6.frequency.register_number(connector=1, channel=1))
    print(pe6.frequency.register_number(connector=1, channel=2))
