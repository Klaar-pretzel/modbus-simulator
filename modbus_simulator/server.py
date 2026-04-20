import asyncio
import logging

from pymodbus.server import ModbusTcpServer
from pymodbus.simulator.simdata import DataType, SimData
from pymodbus.simulator.simdevice import SimDevice

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

HOLDING_REGISTER_FUNC_CODE = 3
DEVICE_ID = 1


async def toggle_register(server: ModbusTcpServer):
    toggle_values = [17, 57]
    index = 0

    while True:
        index = 1 - index
        logger.info(f"Toggling register value to {toggle_values[index]}")
        await server.context.async_setValues(DEVICE_ID, HOLDING_REGISTER_FUNC_CODE, 0, [toggle_values[index]])
        await asyncio.sleep(10)


async def run_server():
    register = SimData(address=0, count=1, values=17, datatype=DataType.UINT16)
    device = SimDevice(id=DEVICE_ID, simdata=register)
    server = ModbusTcpServer(context=device, address=("127.0.0.1", 8002))
    asyncio.create_task(toggle_register(server))
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(run_server())


if __name__ == "__main__":
    asyncio.run(run_server())
