from datetime import datetime
import enum


def enum_formatter(value):
    return value.name


def datetime_formatter(value):
    return value.isoformat() + 'Z'


BASE_FORMATTERS = {
    datetime: datetime_formatter,
    enum.Enum: enum_formatter,
}
