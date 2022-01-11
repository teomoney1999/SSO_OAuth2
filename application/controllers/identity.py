from flask import (
    Blueprint, request, session, url_for,
    jsonify, )
from flask_jwt_extended import jwt_required
from application.database import db
from application.database.model import UserInfo

from application.helper.api import to_dict


bp = Blueprint("identity", __name__)

model = "identity"

# CREATE 
@bp.route(f"/{model}", methods=["POST"])
@jwt_required()
def create(): 
    data = request.get_json()
    
    instance = UserInfo() 
    for key in data: 
        if hasattr(instance, key): 
            setattr(instance, key, data.get(key)) 
    
    db.session.add(instance) 
    db.session.commit()
    return jsonify(to_dict(instance)), 200

# UPDATE
@bp.route(f"/{model}/<id>", methods=["PUT"])
@jwt_required()
def update(id):
    data = request.get_json() 
    
    instance = UserInfo.query.get(id)
    if not instance: 
        return {"error_code": "NOT_FOUND", "error_message": "Can not found!"}, 500
        
    for key in data: 
        if hasattr(instance, key): 
            setattr(instance, key, data.get(key)) 
    db.session.commit() 
    return jsonify(to_dict(instance))

# GET MANY
@bp.route(f"/{model}", methods=["GET"])
@jwt_required()
def get_many():
    instances = UserInfo.query.all()
    result = []
    if not len(instances): 
        return jsonify({"results": result}), 200
    for instance in instances: 
        result.append(to_dict(instance))
    return jsonify({"results": result}), 200

# GET SINGLE
@bp.route(f"/{model}/<id>", methods=["GET"])
@jwt_required()
def get_single(id):
    instance = UserInfo.query.get(id)
    if not instance: 
        return {"error_code": "NOT_FOUND", "error_message": "Can not found!"}, 500
    return jsonify(to_dict(instance)), 200

# DELETE
@bp.route(f"/{model}/<id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    instance = UserInfo.query.get(id)
    if not instance: 
        return {"error_code": "NOT_FOUND", "error_message": "Can not found!"}, 500
    
    db.session.delete(instance)
    db.session.commit()
    return jsonify({}), 200