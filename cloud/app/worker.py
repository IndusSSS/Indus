# app/worker.py
"""
Temporary worker that stays alive and logs a heartbeat.
"""

import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [worker] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

async def main() -> None:
    logger.info("Worker booted – entering heartbeat loop")
    while True:
        logger.info("heartbeat")
        await asyncio.sleep(30)

if __name__ == "__main__":
    # Run the main() coroutine and keep the process alive
    try:
        asyncio.run(main())
    except Exception:
        logger.exception("Worker crashed")
        raise
