from datetime import datetime


def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%d.%m.%Y')


def format_date(date: datetime) -> str:
    return date.strftime('%d.%m.%Y')


def parse_timestamp(timestamp_str: str) -> datetime:
    return datetime.strptime(timestamp_str, '%d.%m.%Y %H:%M:%S.%f')


def format_timestamp(timestamp: datetime) -> str:
    return timestamp.strftime('%d.%m.%Y %H:%M:%S.%f')
