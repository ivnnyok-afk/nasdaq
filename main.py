import logging
import signal

from app.config import load_config
from app.storage import BarStore
from app.stream import run_stream

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("quant-finance-worker")

def main() -> None:
    config = load_config()
    logger.info(
        "Starting worker feed=%s symbols=%d",
        config["feed"], len(config["symbols"])
    )

    store = BarStore(config["database_url"])

    def shutdown(signum, frame) -> None:
        logger.info("Received shutdown signal %s", signum)
        try:
            store.close()
        finally:
            raise SystemExit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    try:
        run_stream(config, store)
    finally:
        try:
            store.close()
        except Exception:
            logger.exception("Error closing database connection")

if __name__ == "__main__":
    main()
