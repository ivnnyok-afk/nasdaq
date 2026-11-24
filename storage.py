import logging
from datetime import timezone

import psycopg

logger = logging.getLogger(__name__)

class BarStore:
    def __init__(self, database_url: str):
        self.conn = psycopg.connect(database_url, autocommit=True)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS market_bars (
                symbol TEXT NOT NULL,
                timeframe TEXT NOT NULL,
                bar_timestamp TIMESTAMPTZ NOT NULL,
                open DOUBLE PRECISION NOT NULL,
                high DOUBLE PRECISION NOT NULL,
                low DOUBLE PRECISION NOT NULL,
                close DOUBLE PRECISION NOT NULL,
                volume DOUBLE PRECISION NOT NULL,
                trade_count BIGINT,
                vwap DOUBLE PRECISION,
                feed TEXT NOT NULL,
                received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                PRIMARY KEY (symbol, timeframe, bar_timestamp)
            )
        """)
        logger.info("Database ready: market_bars table exists")

    def save_minute_bar(self, bar, feed: str) -> None:
        timestamp = bar.timestamp
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        self.conn.execute("""
            INSERT INTO market_bars (
                symbol, timeframe, bar_timestamp, open, high, low, close,
                volume, trade_count, vwap, feed, received_at
            )
            VALUES (%s, '1Min', %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (symbol, timeframe, bar_timestamp) DO UPDATE SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume,
                trade_count = EXCLUDED.trade_count,
                vwap = EXCLUDED.vwap,
                feed = EXCLUDED.feed,
                received_at = NOW()
        """, (
            bar.symbol, timestamp, float(bar.open), float(bar.high),
            float(bar.low), float(bar.close), float(bar.volume),
            int(bar.trade_count) if bar.trade_count is not None else None,
            float(bar.vwap) if bar.vwap is not None else None,
            feed,
        ))

    def close(self) -> None:
        self.conn.close()
