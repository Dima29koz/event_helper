from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity

from . import event_management
from ..models import models
from ..models import views


@event_management.route('/create_event', methods=["POST"])
@jwt_required()
def create_event():
    request_data = request.get_json()
    event = models.Event.create(request_data, current_user)
    if not event:
        return jsonify(msg='Not allowed'), 403
    return jsonify(msg='Event created.', key=event.key)


@event_management.route('/events', methods=["GET"])
@jwt_required()
def get_events():
    event_view = views.EventView(current_user)
    return jsonify(
        creator_on=event_view.get_list(current_user.events),
        member_on=event_view.get_list_with_data(current_user.get_events_where_member())
    )


@event_management.route('/member_info/<event_key>', methods=["GET"])
@jwt_required(optional=True)
def get_member_info(event_key: str):
    event = models.Event.get_by_key(event_key)
    if not event:
        return jsonify(msg='Wrong event key'), 400

    if get_jwt_identity() is None:
        return jsonify(roles=['guest'])

    roles = []
    if current_user == event.creator:
        roles.append('creator')
    member = event.get_member_by_user(current_user)
    if member:
        roles.append(member.role.name)
    if not roles:
        return jsonify(roles=['guest'])
    return jsonify(roles=roles)


@event_management.route('/product/category', methods=["GET", "POST"])
@event_management.route('/product/category/<name>', methods=["GET"])
@jwt_required()
def product_category(name: str = None):
    view = views.ProductCategoryView(current_user)
    if request.method == 'GET':
        if not name:
            return jsonify(view.get_all())
        category = models.ProductCategory.get_by_name(name)
        if not category:
            return jsonify(f'Category `{name}` not found')
        return jsonify(view.get_one(category))

    if request.method == 'POST':
        request_data = request.get_json()
        category = models.ProductCategory.create(request_data.get("name"))
        return jsonify(view.get_one(category))


@event_management.route('/product/type', methods=["GET", "POST"])
@event_management.route('/product/type/<name>', methods=["GET"])
@jwt_required()
def product_type(name: str = None):
    view = views.ProductTypeView(current_user)
    if request.method == 'GET':
        if name is None:
            return jsonify(view.get_all())
        pr_type = models.ProductType.get_by_name(name)
        if not pr_type:
            return jsonify(f'Type `{name}` not found')
        return jsonify(view.get_one(pr_type))

    if request.method == 'POST':
        request_data = request.get_json()
        pr_type = models.ProductType.create(request_data.get("name"))
        return jsonify(view.get_one(pr_type))


@event_management.route('/product/unit', methods=["GET", "POST"])
@event_management.route('/product/unit/<name>', methods=["GET"])
@jwt_required()
def product_unit(name: str = None):
    view = views.ProductUnitView(current_user)
    if request.method == 'GET':
        if name is None:
            return jsonify(view.get_all())
        unit = models.ProductUnit.get_by_name(name)
        if not unit:
            return jsonify(f'Unit `{name}` not found')
        return jsonify(view.get_one(unit))

    if request.method == 'POST':
        request_data = request.get_json()
        unit = models.ProductUnit.create(request_data.get("name"))
        return jsonify(view.get_one(unit))


@event_management.route('/product/base', methods=["GET", "POST"])
@event_management.route('/product/base/<int:product_id>', methods=["GET"])
@jwt_required()
def base_product(product_id: int = None):
    view = views.BaseProductView(current_user)
    if request.method == 'GET':
        if product_id is None:
            return jsonify(view.get_all())
        product = models.BaseProduct.get_by_id(product_id)
        if not product:
            return jsonify(f'Product with id `{product_id}` not found')
        return jsonify(view.get_one(product))

    if request.method == 'POST':
        request_data = request.get_json()
        product = models.BaseProduct.create(request_data)
        if not product:
            return jsonify(msg="Wrong data")
        return jsonify(view.get_one(product))
