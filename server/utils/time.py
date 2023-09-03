from datetime import datetime


def get_date_with_timezone(date_string: str):
    datetime_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f%z')
    return datetime_object


def date_from_str(date_string: str):
    datetime_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    return datetime_object
