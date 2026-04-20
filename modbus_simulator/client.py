import asyncio
import logging
import obsws_python as obs
from pymodbus.client import AsyncModbusTcpClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def run_client():
    try:
        obs_client = obs.ReqClient(host='127.0.0.1', port=4455, password='YRyTnRynNDBatA1m', timeout=3)
        resp = obs_client.get_version()
        logger.info(f"OBS Version: {resp.obs_version}")
    except Exception as e:
        logger.warning(f"OBS connection failed, disabling OBS feature: {e}")
        obs_client = None


    client = AsyncModbusTcpClient("127.0.0.1", port=8002)
    await client.connect()
    recording = False
    try:
        while True:
            result = await client.read_holding_registers(address=0, count=1, device_id=1)
            if result.isError():
                logger.error(f"Error: {result}")
            else:
                value = result.registers[0]
                logger.info(f"Register value: {value}")
                if value == 57 and not recording:
                    if obs_client is not None:
                        try:
                            obs_client.start_record()
                            recording = True
                            logger.info("Recording started")
                        except obs.error.OBSSDKRequestError as e:
                            logger.error(f"Error starting recording: {e}")
                elif value != 57 and recording:
                    if obs_client is not None:
                        try:
                            obs_client.stop_record()
                            recording = False
                            logger.info("Recording stopped")
                        except obs.error.OBSSDKRequestError as e:
                            logger.error(f"Error stopping recording: {e}")
            await asyncio.sleep(1)
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(run_client())
