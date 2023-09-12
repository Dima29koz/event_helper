from . import typefmt
from .tools import filter_foreign_columns, rec_getattr
from ..app.models import models


class BaseView:
    """
    Base Controller

    :param model: db model
    :param current_user: used for setting permissions

    :var column_list:
        Collection of the model field names for the list view.
        If set to `None`, will get them from the model.
    :var column_exclude_list:
        Collection of excluded list column names.
    :var column_details_list:
        Collection of the field names included in the details view.
        If set to `None`, will get them from the model.
    :var column_details_exclude_list:
        Collection of fields excluded from the details view.
    """
    column_display_all_relations = False
    column_display_pk = True
    column_list: tuple[str] = None
    column_exclude_list: tuple[str] = None
    column_details_list: tuple[str] = None
    column_details_exclude_list: tuple[str] = None
    column_formatters = dict()
    column_type_formatters: dict = dict(typefmt.BASE_FORMATTERS)

    def __init__(self, model, current_user: models.User = None):
        self.model = model
        self.current_user = current_user

    def get_one(self, obj):
        columns = self.get_details_columns()
        return {c: self.get_list_value(obj, c) for c in columns}

    def get_list(self, objects):
        columns = self.get_list_columns()
        return [{c: self.get_list_value(obj, c) for c in columns} for obj in objects]

    def get_list_with_data(self, objects):
        columns = self.get_list_columns()
        return [
            {c: self.get_list_value(obj, c) for c in columns} |
            {key: self._get_formatted_value(value) for key, value in data.items()}
            for obj, data in objects
        ]

    def _get_list_value(self, model, name, column_formatters, column_type_formatters):
        value = rec_getattr(model, name)

        column_fmt = column_formatters.get(name)
        if column_fmt:
            value = column_fmt(value)

        value = self._get_formatted_value(value, column_type_formatters)

        return value

    def _get_formatted_value(self, value, column_type_formatters=None):
        if not column_type_formatters:
            column_type_formatters = self.column_type_formatters
        type_fmt = None
        for typeobj, formatter in column_type_formatters.items():
            if isinstance(value, typeobj):
                type_fmt = formatter
                break
        if type_fmt:
            value = type_fmt(value)
        return value

    def get_list_value(self, model, name):
        """
            Returns the value to be displayed in the list view

            :param model:
                Model instance
            :param name:
                Field name
        """
        return self._get_list_value(
            model,
            name,
            self.column_formatters,
            self.column_type_formatters,
        )

    def _scaffold_list_columns(self):
        """
            Return a list of columns from the model.
        """
        columns = []

        for p in self._get_model_iterator():
            if hasattr(p, 'direction'):
                if self.column_display_all_relations or p.direction.name == 'MANYTOONE':
                    columns.append(p.key)
            elif hasattr(p, 'columns'):
                if len(p.columns) > 1:
                    filtered = filter_foreign_columns(self.model.__table__, p.columns)

                    if len(filtered) == 0:
                        continue
                    elif len(filtered) > 1:
                        print('Can not convert multiple-column properties (%s.%s)' % (self.model, p.key))
                        continue

                    column = filtered[0]
                else:
                    column = p.columns[0]

                if column.foreign_keys:
                    continue

                if not self.column_display_pk and column.primary_key:
                    continue

                columns.append(p.key)

        return columns

    def get_list_columns(self):
        """
            Uses `get_column_names` to get a list of the model
            field name for the columns in `column_list`
            and not in `column_exclude_list`. If `column_list` is not set,
            the columns from `scaffold_list_columns` will be used.
        """
        return self._get_column_names(
            only_columns=self.column_list or self._scaffold_list_columns(),
            excluded_columns=self.column_exclude_list,
        )

    def get_details_columns(self):
        """
            Uses `get_column_names` to get a list of the model
            field name for the columns in `column_details_list`
            and not in `column_details_exclude_list`. If `column_details_list`
            is not set, the columns from `scaffold_list_columns` will be used.
        """
        return self._get_column_names(
            only_columns=self.column_details_list or self._scaffold_list_columns(),
            excluded_columns=self.column_details_exclude_list,
        )

    @staticmethod
    def _get_column_names(only_columns, excluded_columns):
        """
            Returns a list of the model field name.

            :param only_columns:
                List of columns to include in the results. If not set,
                `scaffold_list_columns` will generate the list from the model.
            :param excluded_columns:
                List of columns to exclude from the results if `only_columns`
                is not set.
        """
        if excluded_columns:
            only_columns = [c for c in only_columns if c not in excluded_columns]

        return only_columns

    def _get_model_iterator(self, model=None):
        """Return property iterator for the model"""
        if model is None:
            model = self.model

        return model._sa_class_manager.mapper.iterate_properties
