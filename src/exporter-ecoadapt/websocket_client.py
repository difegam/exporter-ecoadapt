import asyncio
import json

import exporter_ecoadapt
from autobahn.asyncio.websocket import (WebSocketClientFactory, WebSocketClientProtocol)


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
            data = exporter_ecoadapt.run_sync_client(port=5020)
            self.sendMessage(json.dumps(data).encode('utf-8'))
            await asyncio.sleep(2)

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':
    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000")
    factory.protocol = WsClientProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, '127.0.0.1', 9000)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
    # -end    # -end    loop.run_forever()
    loop.close()
    # -end    # -end    # -end    # -end