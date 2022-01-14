from flask import (
    Blueprint, request, session, url_for,
    jsonify, )
from werkzeug.security import gen_salt, generate_password_hash
from flask_jwt_extended import jwt_required
from application.database import db
from application.database.model import User

from application.helper.api import to_dict


bp = Blueprint("user", __name__)

model = "user"

def pre_create_user(request): 
    data = request.json 
    salt_length = 32
    data["salt"] = gen_salt(salt_length) 
    data["password"] = generate_password_hash(password=data.get("password"), 
                                              salt_length=salt_length)
    return data

def exclude_columns(instance=None, columns = []): 
    if not instance: 
        return None
    for key in instance: 
        if key in columns: 
            delattr(instance, key)

# CREATE 
@bp.route(f"/{model}", methods=["POST"])
def create(): 
    data = pre_create_user(request)
    instance = User() 
    for key in data: 
        if hasattr(instance, key): 
            setattr(instance, key, data.get(key)) 
    db.session.add(instance) 
    db.session.commit()
    exclude_columns(instance, ["password", "salt", "id"])
    return jsonify(to_dict(instance)), 200

# UPDATE
@bp.route(f"/{model}/<id>", methods=["PUT"])
@jwt_required()
def update(id):
    data = request.get_json() 
    instance = User.query.get(id)
    if not instance: 
        return {"error_code": "NOT_FOUND", "error_message": "Can not found!"}, 500
    for key in data: 
        if hasattr(instance, key): 
            setattr(instance, key, data.get(key)) 
    db.session.commit() 
    exclude_columns(instance, ["password", "salt"])
    return jsonify(to_dict(instance))

# GET MANY
@bp.route(f"/{model}", methods=["GET"])
@jwt_required()
def get_many():
    instances = User.query.all()
    result = []
    if not len(instances): 
        return jsonify({"results": result}), 200
    for instance in instances: 
        exclude_columns(instance, ["password", "salt"])
        result.append(to_dict(instance))
    return jsonify({"results": result}), 200

# GET SINGLE
@bp.route(f"/{model}/<id>", methods=["GET"])
@jwt_required()
def get_single(id):
    instance = User.query.get(id)
    if not instance: 
        return {"error_code": "NOT_FOUND", "error_message": "Can not found!"}, 500
    exclude_columns(instance, ["password", "salt"])
    return jsonify(to_dict(instance)), 200

# DELETE
@bp.route(f"/{model}/<id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    instance = User.query.get(id)
    if not instance: 
        return {"error_code": "NOT_FOUND", "error_message": "Can not found!"}, 500
    db.session.delete(instance)
    db.session.commit()
    return jsonify({}), 200