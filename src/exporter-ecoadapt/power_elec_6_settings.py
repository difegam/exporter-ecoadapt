
PE6_CONFIGURATION = {
    'connectors': 6,
    'channels': 3,
}

# wpb = number of words per bit
PE6_GENERAL_INFORMATION = {
    "software_version": {
        'info': "Software version",
        "wpb": 1,
        "registers_start": 0,
        "registers_end": 0
    },
    "modbus_table_version": {
        'info': "Modbus table version",
        "wpb": 1,
        "registers_start": 1,
        "registers_end": 1
    },
    "mac_address": {
        'info': "MAC address",
        "wpb": 3,
        "registers_start": 2,
        "registers_end": 4
    }
}

# wpc = number of words per channel

PE6_MEASUREMENTS_DEFINITION = {
    "active_energy_import_index": {
        'name': "Active energy Import Index",
        "unit": 'kWh',
        "wpc": 2,
        "registers_start": 28,
        "registers_end": 63
    },
    "reactive_energy_import_index": {
        'name': "Reactive energy import index",
        "unit": 'kVArh',
        "wpc": 2,
        "registers_start": 64,
        "registers_end": 99
    },
    "active_energy_export_index": {
        'name': "Active energy export index",
        "unit": 'kWh',
        "wpc": 2,
        "registers_start": 100,
        "registers_end": 135
    },
    "reactive_energy_export_index": {
        'name': "Reactive energy export index",
        "unit": 'kWh',
        "wpc": 2,
        "registers_start": 136,
        "registers_end": 171
    },
    "active_power": {
        'name': "Active power",
        "unit": 'kWh',
        "wpc": 2,
        "registers_start": 172,
        "registers_end": 207
    },
    "reactive_power": {
        'name': "Reactive power",
        "unit": 'kWh',
        "wpc": 2,
        "registers_start": 208,
        "registers_end": 243
    },
    "power_factor": {
        'name': "Power factor",
        "unit": 'kWh',
        "wpc": 2,
        "registers_start": 244,
        "registers_end": 279
    },
    "rms_current": {
        'name': "RMS current",
        "unit": 'kWh',
        "wpc": 2,
        "registers_start": 280,
        "registers_end": 315
    },
    "rms_current_1_min_average": {
        'name': "RMS current 1 min average",
        "unit": 'kWh',
        "wpc": 2,
        "registers_start": 316,
        "registers_end": 351
    },
    "rms_voltage": {
        'name': "RMS voltage",
        "unit": 'kWh',
        "wpc": 2,
        "registers_start": 352,
        "registers_end": 387
    },
    "rms_voltage_1_min_average": {
        'name': "RMS voltage 1 min average",
        "unit": 'kWh',
        "wpc": 2,
        "registers_start": 388,
        "registers_end": 423
    },
    "frequency": {
        'name': "Frequency",
        "unit": 'kWh',
        "wpc": 2,
        "registers_start": 424,
        "registers_end": 459
    }
}