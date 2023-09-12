from functools import reduce

filter_list = lambda f, l: list(filter(f, l))


def filter_foreign_columns(base_table, columns):
    """
        Return list of columns that belong to passed table.

        :param base_table: Table to check against
        :param columns: List of columns to filter
    """
    return filter_list(lambda c: c.table == base_table, columns)


def rec_getattr(obj, attr, default=None):
    try:
        return reduce(getattr, attr.split('.'), obj)
    except AttributeError:
        return default
