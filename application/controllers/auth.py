from math import floor 
from datetime import datetime, timedelta
from flask import (
    Blueprint, request, redirect, session, url_for,
    jsonify, render_template, make_response)
from werkzeug.security import gen_salt
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_access_cookies)
from application.database import db
from application.database.model import User
from application.helper.api import *
from application.config.cookies import Cookie

bp = Blueprint("auth", __name__)

# TODO: write a worker that clear token that has been expired in USER_LOGIN
@bp.route("/current_user")
@jwt_required()
def get_current_user(): 
    # return the identity of the JWT that is accessing the endpoint
    current_token = get_jwt_identity() 
    print("current_token", current_token)
    return jsonify(current_token=current_token), 200
    
@bp.route(f"/login", methods=["POST"]) 
def login(): 
    data = None
    try:
        data = request.json  
    except: 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Can not read data from request!"}), 500
    
    if not data or "username" not in data: 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Login failed!"}), 500
    
    user = User.query.filter_by(username=data.get("username")).first()
    if not user: 
        return jsonify({"error_code": "NOT_FOUND", "error_message": "User doesn't exist!"})
    
    token = create_access_token(identity={"id": user.id, "username": user.username})
    
    resp = make_response({"id": user.id, "username": user.username})
    set_access_cookies(resp, token)
    return resp, 200

@bp.route(f"/logout", methods=["GET"]) 
@jwt_required()
def logout(): 
    resp = make_response({})
    unset_access_cookies(resp)
    return resp, 200
        
