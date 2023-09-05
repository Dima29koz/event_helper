from flask_socketio import Namespace, join_room, emit, leave_room

from server.app.models import models
from server.common.enums import Role
from server.utils.decorators import keys_required, socket_roles_required as roles_required


class EventManagementNamespace(Namespace):
    @staticmethod
    @keys_required()
    def on_connect(event: models.Event):
        join_room(event.id)
        print('connected')
        emit('connect', dict(data=event.as_dict()))

    @staticmethod
    @keys_required()
    def on_disconnect(event: models.Event):
        leave_room(event.id)
        print('disconnected')

    @staticmethod
    @keys_required(user_token=True)
    @roles_required({Role.organizer, })
    def on_add_member(data, event, current_user):
        member = models.EventMember(data.get('member'))
        event.add_member(member)
        emit('new_member', dict(member=member.as_dict()))

    @staticmethod
    @keys_required(user_token=True)
    @roles_required({Role.organizer, })
    def on_update_member(data, event, current_user):
        member_id = data.get('member').get('id')
        # todo validate
        member = models.EventMember.get_by_id(member_id)
        member.update(data.get('member'))
        emit('update_member', dict(member=member.as_dict()))
