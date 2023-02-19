#!/usr/bin/env python3
"""
A minimal EcoAdapt modbus reader
"""

import argparse
import logging
from typing import List

from modbus_client import ModbusClient
from power_elec_6 import PowerElec6

# configure the client logging
FORMAT = ("%(asctime)-15s %(threadName)-15s "
          "%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s")
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)


def run_sync_client(host: str = "127.0.0.1", port: int = 502, unit: int = 0x1):

    # Setting up Modbus Client
    client = ModbusClient(host, port=port)
    pe6_sensor = PowerElec6()

    read_general_information = [
        pe6_sensor.software_version.registers(),
        pe6_sensor.modbus_table_version.registers(),
        pe6_sensor.mac_address.registers(),
    ]

    for r in read_general_information:
        client.read_input_registers(r[0], r[1], unit=unit)

    registers_data = {}

    # Get registers data - frequency
    read_frequency = pe6_sensor.get_registers_range('frequency')
    registers_data['frequency'] = {
        'values': get_registers_values(client, read_frequency),
        'unit': pe6_sensor.frequency.unit
    }

    # Get registers data - voltage
    read_voltage = pe6_sensor.get_registers_range('rms_voltage')
    registers_data['rms_voltage'] = {
        'values': get_registers_values(client, read_voltage),
        'unit': pe6_sensor.rms_voltage.unit
    }

    # Get registers data - voltage_average
    read_voltage_average = pe6_sensor.get_registers_range('rms_voltage_1_min_average')
    registers_data['rms_voltage_1_min_average'] = {
        'values': get_registers_values(client, read_voltage_average),
        'unit': pe6_sensor.rms_voltage_1_min_average.unit
    }

    # Sent data - WS
    log.info(f"Sending data to server: {registers_data}")

    client.connect()
    client.close()

    return registers_data


def get_registers_values(modbus_client: ModbusClient, registers: List[tuple], unit: int = 0x1):
    return [
        modbus_client.read_input_registers(register[0], register[1], unit=unit) for register in registers if register
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A minimal EcoAdapt modbus reader")
    parser.add_argument("--host", help="modbus Server", type=str, default='localhost')
    parser.add_argument("--port", "-p", help="port to serve (default 502)", type=int, default=5020)
    parser.add_argument("--unit", "-u", help="address device", type=int, default=0x1)

    args = parser.parse_args()
    run_sync_client(args.host, args.port, args.unit)
"""
Output when ran:
>> python3 ./src/exporter-ecoadapt/exporter-ecoadapt.py
2021-03-19 12:31:18,597 MainThread      INFO     exporter-ecoadapt:23       Setting up client
2021-03-19 12:31:18,610 MainThread      INFO     exporter-ecoadapt:27       Reading registers
2021-03-19 12:31:18,615 MainThread      INFO     exporter-ecoadapt:39       (0, 1): ReadRegisterResponse (1): [514]
2021-03-19 12:31:18,622 MainThread      INFO     exporter-ecoadapt:39       (1, 1): ReadRegisterResponse (1): [2]
2021-03-19 12:31:18,635 MainThread      INFO     exporter-ecoadapt:39       (2, 3): ReadRegisterResponse (3): [30, 44285, 17639]
2021-03-19 12:31:18,643 MainThread      INFO     exporter-ecoadapt:39       (244, 12): ReadRegisterResponse (12): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
2021-03-19 12:31:18,646 MainThread      INFO     exporter-ecoadapt:39       (352, 12): ReadRegisterResponse (12): [49709, 17262, 20887, 15905, 45177, 15748, 0, 0, 0, 0, 0, 0]
2021-03-19 12:31:18,650 MainThread      INFO     exporter-ecoadapt:39       (388, 12): ReadRegisterResponse (12): [34030, 17262, 13400, 15907, 22707, 15748, 0, 0, 0, 0, 0, 0]
2021-03-19 12:31:18,654 MainThread      INFO     exporter-ecoadapt:39       (424, 12): ReadRegisterResponse (12): [54339, 16973, 54339, 16973, 43051, 16949, 0, 0, 0, 0, 0, 0]
2021-03-19 12:31:18,655 MainThread      INFO     exporter-ecoadapt:41       Closing client
"""