import asyncio
import argparse
from FwdServer import FwdServer

async def main():
    p = argparse.ArgumentParser()
    p.add_argument('bind', nargs=2)
    args = p.parse_args()

    addr1 = args.bind[0].split(':')
    bind_addr1 = (str(addr1[0]), int(addr1[1]))

    addr2 = args.bind[1].split(':')
    bind_addr2 = (str(addr2[0]), int(addr2[1]))

    s = FwdServer()
    await s.init([(bind_addr1, bind_addr2)])
    await s.start()

if __name__ == "__main__":
    asyncio.run(main())