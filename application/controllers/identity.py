from flask import (
    Blueprint, request, session, url_for,
    jsonify, )
from flask_jwt_extended import jwt_required
from application.database import db
from application.database.model import UserInfo
from application.helper.api import *


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
    user_id = request.args.get('user_id') 
    if user_id: 
        instance = UserInfo.query.filter_by(user_id=user_id).first()
        if not instance: 
            return jsonify({"error_code": "PARAM_ERROR", "error_message": "Not found!"}), 500  
        return jsonify(to_dict(instance)), 200 
    
    instances = UserInfo.query.all()
    results = []
    if not len(instances): 
        return jsonify({"results": results}), 200
    for instance in instances: 
        results.append(to_dict(instance))
    return jsonify({"results": results}), 200

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