###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
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

#
# A local webserver to receive message sent by exporter. For dev and debugging only!
#

import argparse
import asyncio
import logging

from autobahn.asyncio.websocket import (WebSocketServerFactory, WebSocketServerProtocol)

# configure the client logging
FORMAT = ("%(asctime)-15s %(threadName)-15s "
          "%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s")

# configure the client logging
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):

        log.info("Client connecting: {0}".format(request.peer))

        if "WsClientProtocol" in request.protocols:
            self.factory.protocol = 'WsClientProtocol'
            log.info("Subprotocol selected: {}".format(self.factory.protocol))
            return
        else:
            # self.sendClose(404, "No matching protocol")
            return

    async def onOpen(self):
        log.info("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            log.info("Binary message received: {0} bytes".format(len(payload)))
        else:
            log.info("Text message received: {0}".format(payload.decode("utf8")))

        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        log.info("WebSocket connection closed: {0}".format(reason))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A local websocket server that receives and prints messages")
    parser.add_argument("--port", "-p", help="Port to serve (default 9000)", type=int, default=9000)

    args = parser.parse_args()
    server_url = f"ws://127.0.0.1:{args.port}"
    log.info(f"Starting server on {server_url}")
    factory = WebSocketServerFactory(server_url)
    factory.protocol = MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, "0.0.0.0", args.port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        log.warn("Interrupted! Closing server.")
    finally:
        server.close()
        loop.close()
