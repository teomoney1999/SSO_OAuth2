import time
from flask import (
    Blueprint, request, redirect, session, url_for,
    jsonify, render_template, make_response)
from werkzeug.security import gen_salt
from authlib.oauth2 import OAuth2Error
from authlib.integrations.flask_oauth2 import current_token
from application.controllers import USER_LOGIN
from application.database import db
from application.database.model import OAuth2Client
from application.extensions.OAuth2.authorization_server import authorization
from application.helper.api import *


bp = Blueprint("client", __name__)

@bp.route("/client", methods=["POST"]) 
def post(): 
    user = current_user(session=session, request=request) 
    if not user: 
        return jsonify({"error_code": "ACCESS_DENIED", "error_message": "Login required!"}), 500
    
    client_id = gen_salt(24) 
    client_id_issued_at = int(time.time())
    client = OAuth2Client(
        client_id = client_id,
        client_id_issued_at=client_id_issued_at,
        user_id = user.id 
    )
    
    data = request.json 
    keys = ["client_name", "client_uri", "grant_types", "redirect_uris", "response_types", "scope", "token_endpoint_auth_method"]
    client_metadata = {}
    for key in keys:
        if key not in data: 
            continue
        if (key == "token_endpoint_auth_method") and len(data[key]) and (data[key] == "none"): 
            client.client_secret = ''
        elif key == "token_endpoint_auth_method":
            client.client_secret = gen_salt(48)
        client_metadata[key] = data.get(key)
    client.set_client_metadata(client_metadata) 
    
    db.session.add(client) 
    db.session.commit()
    
    return jsonify(to_dict(client)), 200

# @bp.route(f"{prefix}/client")
@bp.route("client", methods=["GET"])
def get_many():
    # TODO: uncomment this
    # user = current_user(session=session, request=request)
    # if not user: 
    #     return jsonify({"error_code": "ACCESS_DENIED", "error_message": "Login required!"}), 500
    instances = OAuth2Client.query.all()
    results = [to_dict(instance) for instance in instances]
    return jsonify({"results": results}), 200


@bp.route("/client/<id>", methods=["GET"])
def get_single(id):
    user = current_user(session=session, request=request)
    if not user: 
        return jsonify({"error_code": "ACCESS_DENIED", "error_message": "Login required!"}), 500
    instance = OAuth2Client.query.get(id)
    return jsonify(to_dict(instance)), 200


@bp.route("/client/<id>", methods=["DELETE"])
def delete(id):
    user = current_user(session=session, request=request)
    if not user: 
        return jsonify({"error_code": "ACCESS_DENIED", "error_message": "Login required!"}), 500
    instance = OAuth2Client.query.get(id)
    
    db.session.delete(instance) 
    db.session.commit()
    return jsonify({}), 200

        
        
    
    
    
    
