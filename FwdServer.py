import asyncio
from typing import Tuple, Coroutine, Any
from ClientServer import ClientServer

Bind = tuple[str, int]

class FwdServer:
    server_pairs: list[tuple[ClientServer, ClientServer]]
    def __init__(self):
        self.server_pairs = []

    async def init(self, server_binds: list[Tuple[Bind, Bind]]):
        for bind1, bind2 in server_binds:
            s1 = ClientServer()
            await s1.init(bind1)

            s2 = ClientServer()
            await s2.init(bind2)

            self.server_pairs.append((s1, s2))

    async def start(self):
        for server1, server2 in self.server_pairs:
            asyncio.create_task(server1.start())
            asyncio.create_task(server2.start())

        monitors = [] # type: list[Coroutine[Any, Any, None]]
        for server1, server2 in self.server_pairs:
            monitors.append(self._monitor(server1, server2))

        errored, _ = await asyncio.wait(monitors, return_when=asyncio.FIRST_EXCEPTION)
        for err in errored:
            err.result()

    async def _monitor(self, s1: ClientServer, s2: ClientServer):
        async def wait_for_data(s: ClientServer, name: str):
            while not s.has_data():
                await asyncio.sleep(0.1)
        while True:
            await asyncio.wait([wait_for_data(s1, "s1"), wait_for_data(s2, "s2")], return_when=asyncio.FIRST_COMPLETED)
            if s1.has_data():
                await s2.send_all(s1.flush_data())
            else:
                await s1.send_all(s2.flush_data())