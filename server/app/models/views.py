from server.app.models import models
from server.common.base_view import BaseView
from server.common.enums import Role
from server.utils.hider import get_hidden_email, get_hidden_pwd
from server.utils.time import date_from_str


class UserView(BaseView):
    column_exclude_list = ('pwd', 'timestamp')
    column_formatters = dict(
        email=get_hidden_email,
        pwd=get_hidden_pwd,
    )

    def __init__(self, current_user):
        super().__init__(models.User, current_user)


class LocationView(BaseView):
    column_list = ('id', 'name')
    column_details_exclude_list = ('creator', )
    column_formatters = dict(
        creator=str,
    )

    def __init__(self, current_user):
        super().__init__(models.Location, current_user)


class EventView(BaseView):
    column_list = ('key', 'title', 'date_start', 'date_end', 'date_tz')
    column_details_exclude_list = ('id', 'key', 'creator')
    column_formatters = dict(
        location=str,
        creator=str,
    )
    column_editable_exclude_list = ('key', )
    column_type_converters = dict(
        date_start=date_from_str,
        date_end=date_from_str
    )

    def __init__(self, current_user):
        super().__init__(models.Event, current_user)


class EventLocationView(BaseView):
    column_list = ('id', 'name')
    column_details_exclude_list = ('id', )

    def __init__(self, current_user):
        super().__init__(models.EventLocation, current_user)


class EventMemberView(BaseView):
    column_exclude_list = ('event', )
    column_details_exclude_list = ('event', )
    column_formatters = dict(
        user=lambda user: str(user) if user else None,
        event=str,
    )
    column_editable_exclude_list = ('money_impact', )
    column_type_converters = dict(
        date_from=date_from_str,
        date_to=date_from_str,
        role=lambda role: Role[role]
    )

    def __init__(self, current_user):
        super().__init__(models.EventMember, current_user)
