# Quant Finance Hub: Market Data Worker

A starter Railway worker that streams Alpaca IEX one-minute stock bars and stores them in Railway PostgreSQL.

## Scope and limitations

- Feed is deliberately fixed to Alpaca IEX (`ALPACA_DATA_FEED=iex`).
- This starter subscribes to up to 30 configured symbols.
- It stores IEX minute bars in PostgreSQL table `market_bars`.
- IEX is not a consolidated all-exchange feed and must not be described as full NASDAQ + NYSE coverage.
- No trading orders are placed by this service.

## Railway setup

Attach this repository to the Railway `Market Data Worker` service and use branch `main`.

Set these variables on **Market Data Worker**, not on the Postgres service:

- `ALPACA_API_KEY`: your Alpaca market-data key
- `ALPACA_SECRET_KEY`: your Alpaca market-data secret
- `ALPACA_DATA_FEED`: `iex`
- `DATABASE_URL`: Railway reference `${{Postgres.DATABASE_URL}}`
- `STOCK_SYMBOLS`: optional comma-separated symbols, maximum 30

Never put real API keys in GitHub. Do not commit `.env`.

## Runtime

Railway starts the process with `python -m app.main`. The worker creates `market_bars` automatically and upserts each received minute bar.

## Local run

1. Use Python 3.11 or newer.
2. Create a local `.env` from `.env.example` and fill it locally.
3. Install: `pip install -r requirements.txt`
4. Export the variables from `.env` in your shell.
5. Run: `python -m app.main`

## Validation

After deployment, check Railway logs for `Connecting to Alpaca IEX minute bars` and `saved_bar`. During market closures there may be no new bars; a successful connection alone does not prove fresh market data is arriving.
