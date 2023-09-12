from flask_socketio import Namespace, join_room, emit, leave_room, send

from server.app.models import models
from server.app.models.views import EventView, EventMemberView
from server.common.enums import Role
from server.utils.decorators import keys_required, socket_roles_required as roles_required


class EventManagementNamespace(Namespace):
    @staticmethod
    @keys_required()
    def on_connect(event: models.Event):
        join_room(event.id)
        send('connected')

    @staticmethod
    @keys_required()
    def on_disconnect(event: models.Event):
        leave_room(event.id)

    @staticmethod
    @keys_required(user_token=True, optional=True)
    def on_get_event_data(data: dict, event: models.Event, current_user: models.User | None):
        emit('get_event_data', dict(event=EventView(current_user).get_one(event)))

    @staticmethod
    @keys_required(user_token=True)
    @roles_required({Role.organizer, })
    def on_update_event_data(data: dict, event: models.Event, current_user: models.User):
        # todo
        emit('update_event_data', dict(data=EventView(current_user).get_one(event)), to=event.id)

    @staticmethod
    @keys_required(user_token=True)
    @roles_required()
    def on_delete_event(data: dict, event: models.Event, current_user: models.User):
        # todo
        emit('delete_event', event.key, to=event.id)

    @staticmethod
    @keys_required(user_token=True, optional=True)
    def on_get_members(data: dict, event: models.Event, current_user: models.User | None):
        # todo
        emit('get_members', event.members)

    @staticmethod
    @keys_required(user_token=True)
    @roles_required({Role.organizer, })
    def on_add_member(data: dict, event: models.Event, current_user: models.User | None):
        member = models.EventMember(data.get('member'))
        event.add_member(member)
        emit('add_member', dict(member=EventMemberView(current_user).get_one(member)), to=event.id)

    @staticmethod
    @keys_required(user_token=True)
    def on_join_event(data: dict, event: models.Event, current_user: models.User):
        # todo
        if data.get('member').get('user_id') != current_user.id:
            raise Exception('Not allowed')
        member = models.EventMember(data.get('member'))
        event.add_member(member)
        emit('add_member', dict(member=EventMemberView(current_user).get_one(member)), to=event.id)

    @staticmethod
    @keys_required(user_token=True)
    @roles_required({Role.organizer, })
    def on_update_member(data: dict, event: models.Event, current_user: models.User):
        member_id = data.get('member').get('id')
        # todo validate
        member = models.EventMember.get_by_id(member_id)
        member.update(data.get('member'))
        emit('update_member', dict(member=EventMemberView(current_user).get_one(member)), to=event.id)

    @staticmethod
    @keys_required(user_token=True)
    @roles_required({Role.organizer, })
    def on_delete_member(data: dict, event: models.Event, current_user: models.User):
        member_id = data.get('member').get('id')
        # todo validate
        member = models.EventMember.get_by_id(member_id)
        member.delete()
        emit('delete_member', member.id, to=event.id)
