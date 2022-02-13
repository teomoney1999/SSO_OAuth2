from math import floor 
from datetime import datetime, timedelta
from flask import (
    Blueprint, request,
    jsonify, make_response)
from werkzeug.security import gen_salt
from authlib.oauth2 import OAuth2Error
from authlib.integrations.flask_oauth2 import current_token
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from application.controllers import USER_LOGIN, USER
from application.database import db
from application.database.model import OAuth2Client, User
from application.extensions.OAuth2.authorization_server import authorization, required_oauth
from application.helper.api import *

bp = Blueprint("oauth2_api", __name__)

model = "oauth2"

@bp.route(f"/{model}/authorize", methods=["GET"])
@jwt_required()
def get_authorize():
    user = get_jwt_identity()
    if not user: 
        return jsonify({"error_code": "ACCESS_DENIED", "error_message": "Login required!"}), 500
    
    end_user = User.query.get(user['id'])
    try: 
        grant = authorization.validate_consent_request(end_user=end_user) 
    except OAuth2Error as error: 
        return jsonify({"error_code": "OAUTH_ERROR", "error_message": f"{error.error}"})
    return jsonify(authorize_payload(user, grant))
    # POST method use for take resource owner confirmation

@bp.route(f"/{model}/authorize", methods=['POST'])
def post_authorize(): 
    data = request.json
    if not data: 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Need confirmation from Resource Owner!"}), 500
    
    grant_user = None
    
    if "user_id" not in data:
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Need user_id in request!"}), 500
    end_user = User.query.get(data.get("user_id"))
    
    if "confirm" not in data: 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Can not get confirmation from Resource Owner!"}), 500
    if data.get("confirm") is True: 
        grant_user = end_user
    return authorization.create_authorization_response(grant_user=grant_user)
    # return authorization.create_authorization_response_with_no_redirect(grant_user=grant_user)


@bp.route(f"/{model}/token", methods=["POST"])
# @jwt_required()
def issue_token(): 
    return authorization.create_token_response()


@bp.route("/api/me") 
# @jwt_required()
@required_oauth("profile")
def find(): 
    user = current_token.user
    return jsonify(username=user.username)
    # data = request.json 
    
    # if "username" in data: 
    #     return jsonify(to_dict(User.query.filter_by(username=data["username"]).first())), 200
    
    # return jsonify({"error_code": "PARAM_ERROR", "error_message": "Not found!"}), 500  
    
        
        