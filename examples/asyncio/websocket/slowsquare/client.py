###############################################################################
##
##  Copyright (C) 2014 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

from autobahn.asyncio.websocket import WebSocketClientProtocol, \
                                       WebSocketClientFactory

import json, random


class SlowSquareClientProtocol(WebSocketClientProtocol):

   def onOpen(self):
      x = 10. * random.random()
      self.sendMessage(json.dumps(x).encode('utf8'))
      print("Request to square {} sent.".format(x))

   def onMessage(self, payload, isBinary):
      if not isBinary:
         res = json.loads(payload.decode('utf8'))
         print("Result received: {}".format(res))
         self.sendClose()

   def onClose(self, wasClean, code, reason):
      if reason:
         print(reason)
      loop.stop()



if __name__ == '__main__':

   try:
      import asyncio
   except ImportError:
      ## Trollius >= 0.3 was renamed
      import trollius as asyncio

   factory = WebSocketClientFactory("ws://localhost:9000", debug = False)
   factory.protocol = SlowSquareClientProtocol

   loop = asyncio.get_event_loop()
   coro = loop.create_connection(factory, '127.0.0.1', 9000)
   loop.run_until_complete(coro)
   loop.run_forever()
   loop.close()
