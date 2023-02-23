import struct
from enum import Enum
from functools import lru_cache
from typing import List

from power_elec_6_settings import (PE6_CONFIGURATION, PE6_GENERAL_INFORMATION, PE6_MEASUREMENTS_DEFINITION)
from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt


class InvalidMeasurementException(Exception):
    "Raised when Measurement does not exist."
    pass


class InvalidConnectorsException(Exception):
    "Raised when Measurement does not exist."
    pass


class InvalidChannelsException(Exception):
    "Raised when Measurement does not exist."
    pass


class GeneralInfo(BaseModel):
    info: str
    wpb: PositiveInt
    registers_start: NonNegativeInt
    registers_end: NonNegativeInt

    def registers(self):
        return self.registers_start, self.wpb


class Measurement(BaseModel):
    name: str
    unit: str
    wpc: PositiveInt
    registers_start: PositiveInt
    registers_end: PositiveInt
    connectors: PositiveInt = Field(default=6)
    channels: PositiveInt = Field(default=3)

    def __hash__(self):
        return hash((self.name, self.wpc, self.registers_start, self.registers_end))

    @lru_cache()
    def _register_number(self, *, connector: int, channel: int):
        """The function for obtaining the register number for connector n channel m"""
        return self.registers_start + ((connector - 1) * 3 + channel - 1) * self.wpc

    def registers(self, *, connector: int, channel: int):

        if connector > self.connectors:
            raise InvalidConnectorsException(f"invalid {connector} number for Power-Elec-6")

        if channel > self.channels:
            raise InvalidChannelsException(f"invalid  {channel} number for Power-Elec-6")

        registers_ch_con = self._register_number(connector=connector, channel=channel)

        return registers_ch_con, self.wpc


class CircuitConfiguration(Enum):
    DISABLED = 0x0000
    SINGLE_PHASE = 0x0001
    THREE_PHASE_WITH_NEUTRAL = 0x0002
    BALANCED_THREE_PHASE_WITH_NEUTRAL = 0x0003
    THREE_PHASE_WITHOUT_NEUTRAL = 0x0004
    BALANCED_THREE_PHASE_NO_NEUTRAL = 0x0005
    THREE_PHASE_WITH_VOLTAGE_TRANSFORMER = 0x0006


def _get_definition(definition: str, sensor_definition: dict) -> dict:

    if definition not in sensor_definition:
        raise InvalidMeasurementException(f"{definition} is not a valid for Power-Elec-6")

    return sensor_definition[definition]


class PowerElec6():

    CONNECTORS = tuple(range(1, PE6_CONFIGURATION.get('connectors', 6) + 1))
    CHANNELS = tuple(range(1, PE6_CONFIGURATION.get('channels', 3) + 1))

    def __init__(self):
        self.software_version = GeneralInfo(**_get_definition('software_version', PE6_GENERAL_INFORMATION))
        self.modbus_table_version = GeneralInfo(**_get_definition('modbus_table_version', PE6_GENERAL_INFORMATION))
        self.mac_address = GeneralInfo(**_get_definition('mac_address', PE6_GENERAL_INFORMATION))

        self.active_energy_import_index = Measurement(
            **_get_definition('active_energy_import_index', PE6_MEASUREMENTS_DEFINITION))
        self.reactive_energy_import_index = Measurement(
            **_get_definition('reactive_energy_import_index', PE6_MEASUREMENTS_DEFINITION))
        self.active_energy_export_index = Measurement(
            **_get_definition('active_energy_export_index', PE6_MEASUREMENTS_DEFINITION))
        self.reactive_energy_export_index = Measurement(
            **_get_definition('reactive_energy_export_index', PE6_MEASUREMENTS_DEFINITION))
        self.active_power = Measurement(**_get_definition('active_power', PE6_MEASUREMENTS_DEFINITION))
        self.reactive_power = Measurement(**_get_definition('reactive_power', PE6_MEASUREMENTS_DEFINITION))
        self.power_factor = Measurement(**_get_definition('power_factor', PE6_MEASUREMENTS_DEFINITION))
        self.rms_current = Measurement(**_get_definition('rms_current', PE6_MEASUREMENTS_DEFINITION))
        self.rms_current_1_min_average = Measurement(
            **_get_definition('rms_current_1_min_average', PE6_MEASUREMENTS_DEFINITION))
        self.rms_voltage = Measurement(**_get_definition('rms_voltage', PE6_MEASUREMENTS_DEFINITION))
        self.rms_voltage_1_min_average = Measurement(
            **_get_definition('rms_voltage_1_min_average', PE6_MEASUREMENTS_DEFINITION))
        self.frequency = Measurement(**_get_definition('frequency', PE6_MEASUREMENTS_DEFINITION))

    def get_registers_range(self, measurement: str):
        if measurement not in self.__dict__:
            return []
        return [(self.__dict__[measurement]._register_number(connector=1, channel=1), 12)]

    def _get_big_endian_measurements(self, measurements: List[int], wpc: int):
        return (tuple(measurements[i:i + wpc]) for i in range(0, len(measurements), wpc))

    def _hex2float(self, measurements):

        if not all(measurements):
            return 0

        hex_values = [hex(value)[2:] for value in list(measurements)[::-1]]
        hex_values_as_str = ''.join(hex_values)

        return struct.unpack('!f', bytes.fromhex(hex_values_as_str))[0]

    def get_float_value(self, measurements: List[int], wpc: int, precision=3):
        measurements_tuples = self._get_big_endian_measurements(measurements, wpc)
        return [round(self._hex2float(measurements_values), precision) for measurements_values in measurements_tuples]


if __name__ == "__main__":
    pass
# w