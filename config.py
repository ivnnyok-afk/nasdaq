import os

DEFAULT_SYMBOLS = (
    "AAPL,MSFT,NVDA,AMZN,GOOGL,META,TSLA,AVGO,BRK.B,LLY,"
    "JPM,V,MA,ORCL,COST,HD,PG,JNJ,ABBV,CRM,NFLX,AMD,CVX,"
    "KO,MRK,PEP,ADBE,WMT,CSCO,ACN"
)

def required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

def load_symbols() -> list[str]:
    raw = os.getenv("STOCK_SYMBOLS", DEFAULT_SYMBOLS)
    symbols = list(dict.fromkeys(
        item.strip().upper() for item in raw.split(",") if item.strip()
    ))
    if not symbols:
        raise RuntimeError("STOCK_SYMBOLS must contain at least one symbol")
    if len(symbols) > 30:
        raise RuntimeError(
            f"This IEX starter is capped at 30 symbols; received {len(symbols)}"
        )
    return symbols

def load_config() -> dict:
    feed = os.getenv("ALPACA_DATA_FEED", "iex").strip().lower()
    if feed != "iex":
        raise RuntimeError("This starter is restricted to ALPACA_DATA_FEED=iex")
    return {
        "api_key": required_env("ALPACA_API_KEY"),
        "secret_key": required_env("ALPACA_SECRET_KEY"),
        "database_url": required_env("DATABASE_URL"),
        "feed": feed,
        "symbols": load_symbols(),
    }
