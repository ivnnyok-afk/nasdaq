import logging

from alpaca.data.enums import DataFeed
from alpaca.data.live import StockDataStream

logger = logging.getLogger(__name__)

def run_stream(config: dict, store) -> None:
    stream = StockDataStream(
        api_key=config["api_key"],
        secret_key=config["secret_key"],
        feed=DataFeed.IEX,
    )

    async def on_bar(bar) -> None:
        try:
            store.save_minute_bar(bar, feed="iex")
            logger.info(
                "saved_bar symbol=%s ts=%s close=%s",
                bar.symbol, bar.timestamp.isoformat(), bar.close
            )
        except Exception:
            logger.exception("Could not persist bar for %s", getattr(bar, "symbol", "?"))
            raise

    stream.subscribe_bars(on_bar, *config["symbols"])
    logger.info(
        "Connecting to Alpaca IEX minute bars for %d symbols: %s",
        len(config["symbols"]), ",".join(config["symbols"])
    )
    stream.run()
