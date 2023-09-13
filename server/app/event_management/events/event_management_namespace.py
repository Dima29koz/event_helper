from flask_socketio import Namespace, join_room, emit, leave_room, send

from server.app.models.models import Event, User, EventMember
from server.app.models.views import EventView, EventLocationView, EventMemberView
from server.common.enums import Role, EntityType
from server.utils.decorators import keys_required, socket_roles_required as roles_required


class EventManagementNamespace(Namespace):
    @staticmethod
    @keys_required()
    def on_connect(event: Event):
        join_room(event.id)
        send('connected')

    @staticmethod
    @keys_required()
    def on_disconnect(event: Event):
        leave_room(event.id)

    @staticmethod
    @keys_required(user_token=True, optional=True)
    def on_get_data(data: dict, event: Event, current_user: User | None):
        match data.get('entity'):
            case EntityType.event.name:
                emit('get_event', EventView(current_user).get_one(event))
            case EntityType.location.name:
                emit('get_event_location', EventLocationView(current_user).get_one(event.location))
            case EntityType.members.name:
                emit('get_event_members', EventMemberView(current_user).get_list(event.members))
            case _:
                emit('error', 'NotImplemented')

    @staticmethod
    @keys_required(user_token=True)
    @roles_required({Role.organizer, })
    def on_update_data(data: dict, event: Event, current_user: User):
        match data.get('entity'):
            case EntityType.event.name:
                view = EventView(current_user)
                if view.update(event, data.get('data')):
                    emit('update_event', view.get_one(event), to=event.id)
            case EntityType.location.name:
                view = EventLocationView(current_user)
                location = event.location
                if view.update(location, data.get('data')):
                    emit('update_event_location', view.get_one(location), to=event.id)
            case _:
                emit('error', 'NotImplemented')

    @staticmethod
    @keys_required(user_token=True)
    @roles_required()
    def on_delete_event(data: dict, event: Event, current_user: User):
        # todo
        emit('delete_event', event.key, to=event.id)

    @staticmethod
    @keys_required(user_token=True)
    @roles_required({Role.organizer, })
    def on_add_member(data: dict, event: Event, current_user: User | None):
        member = EventMember(data.get('member'))
        event.add_member(member)
        emit('add_member', dict(member=EventMemberView(current_user).get_one(member)), to=event.id)

    @staticmethod
    @keys_required(user_token=True)
    def on_join_event(data: dict, event: Event, current_user: User):
        # todo
        if data.get('member').get('user_id') != current_user.id:
            raise Exception('Not allowed')
        member = EventMember(data.get('member'))
        event.add_member(member)
        emit('add_member', dict(member=EventMemberView(current_user).get_one(member)), to=event.id)

    @staticmethod
    @keys_required(user_token=True)
    @roles_required({Role.organizer, })
    def on_update_member(data: dict, event: Event, current_user: User):
        member_id = data.get('member').get('id')
        # todo validate
        member = EventMember.get_by_id(member_id)
        member.update(data.get('member'))
        emit('update_member', dict(member=EventMemberView(current_user).get_one(member)), to=event.id)

    @staticmethod
    @keys_required(user_token=True)
    @roles_required({Role.organizer, })
    def on_delete_member(data: dict, event: Event, current_user: User):
        member_id = data.get('member').get('id')
        # todo validate
        member = EventMember.get_by_id(member_id)
        member.delete()
        emit('delete_member', member.id, to=event.id)
