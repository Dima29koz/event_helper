from flask import request, session
from flask_jwt_extended import decode_token
from flask_socketio import Namespace, join_room, emit, leave_room, send

from server.app.models.models import Event, User, EventMember, Product
from server.app.models.views import EventView, EventLocationView, EventMemberView, EventProductView
from server.common.enums import Role, EntityType
from server.common.exceptions import MemberWithGivenUserIDExists
from server.utils.decorators import (
    socket_roles_required as roles_required,
    event_required,
    user_required
)


class EventManagementNamespace(Namespace):
    @staticmethod
    @event_required
    def on_connect(event: Event):
        join_room(event.id)
        if 'sid_to_user_id' not in session:
            session['sid_to_user_id'] = dict()

        token = request.cookies.get('access_token_cookie')
        csrf_token = request.cookies.get('csrf_access_token')
        current_user = None
        if token and csrf_token:
            token_data = decode_token(token, csrf_token)
            current_user = User.get_by_id(token_data.get("sub"))

        session['sid_to_user_id'].update({request.sid: current_user.id if current_user else None})
        send('connected')

    @staticmethod
    @event_required
    def on_disconnect(event: Event):
        leave_room(event.id)
        session['sid_to_user_id'].pop(request.sid, None)

    @staticmethod
    @event_required
    @user_required(optional=True)
    def on_get_data(data: dict, event: Event, current_user: User | None):
        match data.get('entity'):
            case EntityType.event.name:
                emit('get_event', EventView(current_user).get_one(event))
            case EntityType.location.name:
                emit('get_event_location', EventLocationView(current_user).get_one(event.location))
            case EntityType.members.name:
                emit('get_event_members', EventMemberView(current_user).get_list(event.members))
            case EntityType.products.name:
                emit('get_event_products', EventProductView(current_user).get_list(event.products))
            case _:
                emit('error', 'NotImplemented')

    @staticmethod
    @event_required
    @user_required()
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

            case EntityType.product.name:
                product = event.get_product_by_id(entity_data.pop('id', None))
                EventManagementNamespace._update_product(product, entity_data, event, current_user)

            case _:
                emit('error', 'NotImplemented')

    @staticmethod
    @event_required
    @user_required()
    @roles_required()
    def on_delete_event(_: dict, event: Event, current_user: User):
        event_id, key = event.delete()
        emit('delete_event', dict(id=event_id, key=key), to=event.id)

    @staticmethod
    @event_required
    @user_required()
    @roles_required({Role.organizer, })
    def on_add_member(data: dict, event: Event, current_user: User | None):
        EventManagementNamespace._add_member(data.get('member'), event, current_user)

    @staticmethod
    @event_required
    @user_required()
    def on_join_event(data: dict, event: Event, current_user: User):
        member_data = data.get('member')
        member_data['role'] = Role.member.name
        member_data['user_id'] = current_user.id
        EventManagementNamespace._add_member(member_data, event, current_user)

    @staticmethod
    @event_required
    @user_required()
    def on_update_me(data: dict, event: Event, current_user: User):
        data.pop('user_id', None)
        member_data = data.get('data')
        member = event.get_member_by_user(current_user)
        if member.role is Role.member and event.creator != current_user:
            member_data.pop('role', None)

        EventManagementNamespace._update_member(member, member_data, event, current_user)

    @staticmethod
    @event_required
    @user_required()
    def on_delete_me(_, event: Event, current_user: User):
        member = event.get_member_by_user(current_user)
        EventManagementNamespace._delete_member(member, event)

    @staticmethod
    @event_required
    @user_required()
    @roles_required({Role.organizer, })
    def on_delete_member(data: dict, event: Event, current_user: User):
        member = event.get_member_by_id(data.get('member_id'))
        EventManagementNamespace._delete_member(member, event)

    @staticmethod
    @event_required
    @user_required()
    @roles_required({Role.organizer, })
    def on_set_member_money(data: dict, event: Event, current_user: User):
        entity_data: dict = data.get('data')
        member = event.get_member_by_id(entity_data.get('id'))
        member.set_money_impact(entity_data.get('money_impact'))
        view = EventMemberView(current_user)
        emit('update_event_member', view.get_one(member), to=event.id)

    @staticmethod
    @event_required
    @user_required()
    @roles_required({Role.organizer, })
    def on_add_product(data: dict, event: Event, current_user: User):
        product, updated_product = event.add_product(data.get('product'))
        if product:
            emit('add_product', EventProductView(current_user).get_one(product), to=event.id)
        if updated_product:
            emit('update_event_product', EventProductView(current_user).get_one(product), to=event.id)

    @staticmethod
    @event_required
    @user_required()
    @roles_required({Role.organizer, })
    def on_add_products(data: dict, event: Event, current_user: User):
        added_products, updated_products = event.add_products(data.get('products'))
        if added_products:
            emit(
                'add_products',
                EventProductView(current_user).get_list(added_products),
                to=event.id
            )
        if updated_products:
            emit(
                'update_event_products',
                EventProductView(current_user).get_list(updated_products),
                to=event.id
            )

    @staticmethod
    @event_required
    @user_required()
    @roles_required({Role.organizer, })
    def on_delete_event_product(data: dict, event: Event, current_user: User):
        product = event.get_product_by_id(data.get('product_id'))
        product_id = product.delete()
        emit('delete_event_product', dict(product_id=product_id), to=event.id)

    @staticmethod
    def _add_member(member_data: dict, event: Event, current_user: User | None):
        try:
            member = event.add_member(member_data)
        except MemberWithGivenUserIDExists as e:
            emit('error', e.args)
            return

        if not member:
            emit('error', 'Bad member`s data')
        else:
            view = EventMemberView(current_user)
            emit('add_member', view.get_one(member), to=event.id)

    @staticmethod
    def _update_member(member: EventMember | None, member_data: dict, event: Event, current_user: User):
        if not member:
            emit('error', 'Member not found')
            return
        view = EventMemberView(current_user)
        if view.update_obj(member, member_data):
            emit('update_event_member', view.get_one(member), to=event.id)

    @staticmethod
    def _update_product(product: Product | None, product_data: dict, event: Event, current_user: User):
        if not product:
            emit('error', 'Product not found')
            return
        view = EventProductView(current_user)
        if view.update_obj(product, product_data):
            emit('update_event_product', view.get_one(product), to=event.id)

    @staticmethod
    def _delete_member(member: EventMember, event: Event):
        if not member:
            emit('error', 'Member not found')
            return
        member_id = member.delete()
        emit('delete_member', dict(member_id=member_id), to=event.id)
