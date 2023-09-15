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
        entity_data: dict = data.get('data')
        match data.get('entity'):
            case EntityType.event.name:
                view = EventView(current_user)
                if view.update_obj(event, entity_data):
                    emit('update_event', view.get_one(event), to=event.id)

            case EntityType.location.name:
                view = EventLocationView(current_user)
                location = event.location
                if view.update_obj(location, entity_data):
                    emit('update_event_location', view.get_one(location), to=event.id)

            case EntityType.member.name:
                member = event.get_member_by_id(entity_data.pop('id', None))
                EventManagementNamespace._update_member(member, entity_data, event, current_user)

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
        EventManagementNamespace._add_member(data.get('member'), event, current_user)

    @staticmethod
    @keys_required(user_token=True)
    def on_join_event(data: dict, event: Event, current_user: User):
        member_data = data.get('member')
        member_data['role'] = Role.member.name
        member_data['user_id'] = current_user.id
        EventManagementNamespace._add_member(member_data, event, current_user)

    @staticmethod
    @keys_required(user_token=True)
    def on_update_me(data: dict, event: Event, current_user: User):
        member_data = data.get('data')
        member_data.pop('role', None)
        member = event.get_member_by_user(current_user)
        EventManagementNamespace._update_member(member, member_data, event, current_user)

    @staticmethod
    @keys_required(user_token=True)
    @roles_required({Role.organizer, })
    def on_delete_member(data: dict, event: Event, current_user: User):
        member_id = data.get('member').get('id')
        # todo validate
        member = EventMember.get_by_id(member_id)
        member.delete()
        emit('delete_member', member.id, to=event.id)

    @staticmethod
    def _add_member(member_data: dict, event: Event, current_user: User | None):
        member = event.add_member(member_data)
        if not member:
            emit('error', 'Bad member`s data')
        else:
            view = EventMemberView(current_user)
            emit('add_member', view.get_one(member), to=event.id)

    @staticmethod
    def _update_member(member: EventMember, member_data: dict, event: Event, current_user: User):
        if not member:
            emit('error', 'Member not found')
            return
        view = EventMemberView(current_user)
        if view.update_obj(member, member_data):
            emit('update_event_member', view.get_one(member), to=event.id)
