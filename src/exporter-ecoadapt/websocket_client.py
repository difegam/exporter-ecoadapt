###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) typedef int GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

import argparse
import asyncio
import json
import logging

import exporter_ecoadapt
from autobahn.asyncio.websocket import (WebSocketClientFactory, WebSocketClientProtocol)
from modbus_client import ModbusClient
from power_elec_6 import PowerElec6
from shared import FORMAT

# configure the client logging
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)


class WsClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        log.info(f"Server connected: {response.peer}")
        headers = {"Server": "MyServer", "Sec-WebSocket-Protocol": "WsClientProtocol", "Sec-WebSocket-Version": "13"}
        return headers

    def onConnecting(self, transport_details):
        log.info(f"Connecting; transport details: {transport_details}")
        return None

    async def onOpen(self):
        log.info("WebSocket connection open.")

        # Setting up Modbus Client
        client = ModbusClient(args.modbushost, args.modbusport)

        # Crate a PE& Tcp Client definition
        pe6_sensor = PowerElec6()

        # start sending messages every n second ..
        while True:
            try:
                data = exporter_ecoadapt.run_sync_client(
                    client,
                    pe6_sensor,
                    args.unit,
                )

                self.sendMessage(json.dumps(data).encode('utf-8'))
                await asyncio.sleep(args.time)

            except Exception as e:
                log.error(f"Error occurred in {type(e).__name__}: {str(e)}")

    def onMessage(self, payload, isBinary):
        if isBinary:
            log.info("Binary message received: {0} bytes".format(len(payload)))
        else:
            log.info("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        log.info("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':
    # tcp server arguments
    parser = argparse.ArgumentParser(description="A minimal WebSocket Client")
    parser.add_argument("--server", help="server address", type=str, default='127.0.0.1')
    parser.add_argument("--port", "-p", help="port to server (default 9000)", type=int, default=9000)

    #  modbus arguments
    parser.add_argument("--modbushost", "-mh", help="modbus Server", type=str, default='localhost')
    parser.add_argument("--modbusport", "-mp", help="port to serve (default 502)", type=int, default=502)
    parser.add_argument("--unit", "-u", help="address device", type=int, default=0x1)

    parser.add_argument(
        "--time",
        "-t",
        help="time in seconds between each reading/sending of messages to the server (default 5 seconds)",
        type=int,
        default=5)

    args = parser.parse_args()

    factory = WebSocketClientFactory(f"ws://{args.server}:{args.port}")
    factory.protocol = WsClientProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, args.server, args.port)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
    # -end
