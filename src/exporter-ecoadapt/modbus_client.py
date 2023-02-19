import logging

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ConnectionException, ModbusException

# configure the client logging
FORMAT = ("%(asctime)-15s %(threadName)-15s "
          "%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s")
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)


class ModbusClient(object):

    def __init__(self, host: str = 'localhost', port: int = 502):
        self.host = host
        self.port = port

        self.client = ModbusTcpClient(host=host, port=port)
        log.info("Setting up client")

    def read_coils(self, address, count, **kwargs):

        try:
            response = self.client.read_coils(address, count, **kwargs)
            log.info("%s: %s: %s" % (response, response, response.bits))
            return response.bits

        except ModbusException as mb_error:
            log.error(f"Error occurred in {type(mb_error).__name__}: {str(mb_error)}")

        finally:
            self.client.close()

    def read_inputs(self, address, count, **kwargs):

        try:
            response = self.client.read_discrete_inputs(address, count, **kwargs)
            log.info("%s: %s: %s" % (response, response, response.bits))
            return response.bits

        except ModbusException as mb_error:
            log.error(f"Error occurred in {type(mb_error).__name__}: {str(mb_error)}")

        finally:
            self.client.close()

    def read_holding_registers(self, address, count, **kwargs):

        try:
            log.info("Reading registers")
            response = self.client.read_holding_registers(address, count, **kwargs)
            log.info("%s: %s: %s" % (response, response, response.registers))
            return response.registers

        except ModbusException as mb_error:
            log.error(f"Error occurred in {type(mb_error).__name__}: {str(mb_error)}")

        finally:
            self.client.close()

    def read_input_registers(self, address, count, **kwargs):

        try:
            response = self.client.read_input_registers(address, count, **kwargs)
            log.info("%s: %s: %s" % ((address, count), response, response.registers))
            return response.registers

        except ModbusException as mb_error:
            log.error(f"Error occurred in {type(mb_error).__name__}: {str(mb_error)}")

        except Exception as e:
            log.error(f"Error occurred in {type(e).__name__}: {str(e)}")

        finally:
            self.client.close()

    def write_coil(self, address, value):

        try:
            response = self.client.write_coil(address, value)
            log.info("%s: %s: %s" % (response, response, response.function_code))
            return response.function_code

        except ModbusException as mb_error:
            log.error(f"Error occurred in {type(mb_error).__name__}: {str(mb_error)}")

        finally:
            self.client.close()

    def write_register(self, address, value):

        try:
            response = self.client.write_register(address, value)
            log.info("%s: %s: %s" % (response, response, response.function_code))
            return response.function_code

        except ModbusException as mb_error:
            log.error(f"Error occurred in {type(mb_error).__name__}: {str(mb_error)}")

        finally:
            self.client.close()

    def write_coils(self, address, values):

        try:
            response = self.client.write_coils(address, values)
            log.info("%s: %s: %s" % (response, response, response.function_code))
            return response.function_code

        except ModbusException as mb_error:
            log.error(f"Error occurred in {type(mb_error).__name__}: {str(mb_error)}")
        finally:
            self.client.close()

    def write_registers(self, address, values):

        try:
            response = self.client.write_registers(address, values)
            log.info("%s: %s: %s" % (response, response, response.function_code))
            return response.function_code

        except ModbusException as mb_error:
            log.error(f"Error occurred in {type(mb_error).__name__}: {str(mb_error)}")

        finally:
            self.client.close()

    def connect(self):
        log.info(f"Connecting to {self.host}:{self.port}")
        try:
            if not self.client.connect():
                raise ConnectionException("Failed to connect to Modbus server")

            log.info("Connecting succeeded")

        except ConnectionException as mb_error:
            log.error(f"Error on connect: {str(mb_error)}")

    def close(self):
        log.info("Closing client connection")
        self.client.close()


if __name__ == "__main__":
    mbc = ModbusClient()
    mbc.connect()