#!/usr/bin/env python3
"""
A minimal EcoAdapt modbus reader
"""

import argparse
import logging
from typing import List

from modbus_client import ModbusClient
from power_elec_6 import PowerElec6
from shared import FORMAT

# configure the client logging
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)


def run_sync_client(modbus_client: ModbusClient, tcp_modbus_sensor: PowerElec6, unit: int = 0x1):

    registers_data = {}

    #  Confecting to Modbus Sever
    modbus_client.connect()

    # reading sensor general information
    read_general_information = [
        tcp_modbus_sensor.software_version.registers(),
        tcp_modbus_sensor.modbus_table_version.registers(),
        tcp_modbus_sensor.mac_address.registers(),
    ]

    for r in read_general_information:
        modbus_client.read_input_registers(r[0], r[1], unit=unit)

    # Get registers data - frequency
    read_frequency = tcp_modbus_sensor.get_registers_range('frequency')
    registers_data['frequency'] = {
        'values': get_registers_values(modbus_client, read_frequency),
        'unit': tcp_modbus_sensor.frequency.unit
    }

    # Get registers data - voltage
    read_voltage = tcp_modbus_sensor.get_registers_range('rms_voltage')
    registers_data['rms_voltage'] = {
        'values': get_registers_values(modbus_client, read_voltage),
        'unit': tcp_modbus_sensor.rms_voltage.unit
    }

    # Get registers data - voltage_average
    read_voltage_average = tcp_modbus_sensor.get_registers_range('rms_voltage_1_min_average')
    registers_data['rms_voltage_1_min_average'] = {
        'values': get_registers_values(modbus_client, read_voltage_average),
        'unit': tcp_modbus_sensor.rms_voltage_1_min_average.unit
    }

    # Close modbus connection
    modbus_client.close()

    log.debug(f"Register data: {registers_data}")

    return registers_data


def get_registers_values(modbus_client: ModbusClient, registers: List[tuple], unit: int = 0x1):
    return [
        modbus_client.read_input_registers(register[0], register[1], unit=unit) for register in registers if register
    ]


if __name__ == "__main__":
    # TODO: allow the selection of the measurements to be read
    parser = argparse.ArgumentParser(description="A minimal EcoAdapt modbus reader")
    parser.add_argument("--host", help="modbus Server", type=str, default='localhost')
    parser.add_argument("--port", "-p", help="port to serve (default 502)", type=int, default=5020)
    parser.add_argument("--unit", "-u", help="address device", type=int, default=0x1)

    args = parser.parse_args()

    # Setting up Modbus Client
    client = ModbusClient(args.host, args.port)

    # Crate a PE& Tcp Client definition
    pe6_sensor = PowerElec6()

    run_sync_client(
        client,
        pe6_sensor,
        args.unit,
    )
