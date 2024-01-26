from datetime import datetime


def parse_timestamp(timestamp_str: str) -> float:
    return datetime.fromisoformat(timestamp_str).timestamp()


def format_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).isoformat()
