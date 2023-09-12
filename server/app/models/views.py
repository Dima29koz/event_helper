from server.app.models import models
from server.common.base_view import BaseView
from server.utils.hider import get_hidden_email, get_hidden_pwd


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
    column_formatters = dict(
        location=str,
        creator=str,
    )

    def __init__(self, current_user):
        super().__init__(models.Event, current_user)


class EventMemberView(BaseView):
    column_exclude_list = ('event', )
    column_formatters = dict(
        user=str,
        event=str,
    )

    def __init__(self, current_user):
        super().__init__(models.EventMember, current_user)
