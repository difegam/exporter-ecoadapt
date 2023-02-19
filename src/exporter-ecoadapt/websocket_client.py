import argparse
import asyncio
import json
import logging

import exporter_ecoadapt
from autobahn.asyncio.websocket import (WebSocketClientFactory, WebSocketClientProtocol)

# configure the client logging
FORMAT = ("%(asctime)-15s %(threadName)-15s "
          "%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s")
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)


class WsClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print(f"Server connected: {response.peer}")

        headers = {"Server": "MyServer", "Sec-WebSocket-Protocol": "WsClientProtocol", "Sec-WebSocket-Version": "13"}

        return headers

    def onConnecting(self, transport_details):
        print(f"Connecting; transport details: {transport_details}")
        return None

    async def onOpen(self):
        print("WebSocket connection open.")

        # start sending messages every second ..
        while True:
            try:
                data = exporter_ecoadapt.run_sync_client(port=5020)
                self.sendMessage(json.dumps(data).encode('utf-8'))
                await asyncio.sleep(2)

            except Exception as e:
                log.error(f"Error occurred in {type(e).__name__}: {str(e)}")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A minimal WebSocket Client")
    parser.add_argument("--server", help="server", type=str, default='127.0.0.1')
    parser.add_argument("--port", "-p", help="port to serve (default 9000)", type=int, default=9000)

    args = parser.parse_args()

    factory = WebSocketClientFactory(f"ws://{args.server}:{args.port}")
    factory.protocol = WsClientProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, args.server, args.port)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
    # -end
    # -end
