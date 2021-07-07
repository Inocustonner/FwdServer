import asyncio
from asyncio.base_events import Server
from typing import NamedTuple, Tuple

MAX_DATA_LEN=1024 * 10

class Client(NamedTuple):
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter

class ClientServer:
    _data: bytes
    server: Server
    clients: list[Client]

    def __init__(self):
        self.clients = []
        self._data = b""

    async def init(self, bind_addr: Tuple[str, int]):
        self.server = await asyncio.start_server(self._handle, *bind_addr)

    async def start(self):
        async with self.server:
            await self.server.serve_forever()

    def has_data(self) -> bool:
        return self._data != b""

    def flush_data(self) -> bytes:
        data = self._data
        self._data = b""
        return data

    async def send_all(self, data: bytes):
        for client in self.clients:
            if not client.writer.is_closing():
                client.writer.write(data)
                await client.writer.drain()

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        print('New client', writer.get_extra_info('peername'))

        client = Client(reader, writer)
        self.clients.append(client)
        await self._serve_client(client)
        self.clients.remove(client)
        client.writer.close()
        await client.writer.wait_closed()

        print('Removed client', writer.get_extra_info('peername'))

    async def _serve_client(self, client: Client):
        while True:
            data, closed = await self._read_available(client)
            if len(self._data) > MAX_DATA_LEN:
                self._data = data
            else:
                self._data += data
            if closed:
                return

    async def _read_available(self, client: Client) -> Tuple[bytes, bool]:
        one = await client.reader.read(1)
        if one == b"":
            return one, True
        buf = b"" + one
        while True:
            try:
                one = await asyncio.wait_for(client.reader.read(1), 0.1)
                buf += one
                if one == b"":
                    return buf, True
            except asyncio.TimeoutError:
                break
        return buf, False