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
from application.database.model import OAuth2Client, User, UserInfo, OAuth2Token
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

@bp.route(f"/{model}/implicit/authorize", methods=["GET"])
@jwt_required()
def implicit_authorize():
    user = get_jwt_identity()
    if not user: 
        return jsonify({"error_code": "ACCESS_DENIED", "error_message": "Login required!"}), 500
    end_user = User.query.get(user['id'])
    return authorization.create_authorization_response(grant_user=end_user)
    # POST method use for take resource owner confirmation
    

@bp.route(f"/{model}/authorize", methods=['POST'])
def post_authorize(): 
    data = request.form
    if not data: 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Need confirmation from Resource Owner!"}), 500
    
    if "user_id" not in data:
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Need user_id in request!"}), 500
    end_user = User.query.get(data.get("user_id"))
    
    if "confirm" not in data: 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Can not get confirmation from Resource Owner!"}), 500
    if data.get('confirm') != 'true':
        grant_user = None
    else: 
        grant_user = end_user
    return authorization.create_authorization_response(grant_user=grant_user)
    # return authorization.create_authorization_response_with_no_redirect(grant_user=grant_user)


@bp.route(f"/{model}/token", methods=["POST"])
# @jwt_required()
def issue_token(): 
    return authorization.create_token_response()


def _get_info(keys, user_id):
    identity = UserInfo.query.filter_by(user_id=user_id).first() 
    if not identity: 
        return None 
    
    info = {} 
    for key in keys: 
        if hasattr(identity, key): 
            info[key] = getattr(identity, key, None)
    return info 

def _check_credentials(current_token): # return user_id
    user_id = current_token.user_id
    if user_id: 
        return user_id 
    
    client_id = current_token.client_id
    if client_id: 
        client = OAuth2Client.query.filter_by(client_id=client_id).first() 
        if not client: 
            return None
        return client.user_id
    
    return None

# BASIC PROFILE
# - name
# - email
# - gender
basic_keys = ['full_name', 'email', 'gender']

        
# DETAIL PROFILE
# - super(BASIC PROFILE)
# - date of birth
# - phone number
# - address 
detail_keys = ['date_birth', 'phone_number', 'address']


# LEGAL PROFILE
# - super(DETAIL PROFILE) 
# - ID number
# - Previous ID number
# - Date Register
legal_keys = ['id_number', 'previous_id_number', 'date_register']

@bp.route(f"/{model}/info/profile") 
@required_oauth("profile")
def find_basic_info(): 
    user_id = _check_credentials(current_token=current_token)
    if not user_id: 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "user_id required!"}), 500
    
    infos = _get_info(basic_keys, user_id)
    if not infos: 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Not found!"}), 500 
    return jsonify(infos), 200

@bp.route(f"/{model}/info/detail") 
@required_oauth("detail")
def find_detail_info(): 
    user_id = _check_credentials(current_token=current_token)
    if not user_id: 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "user_id required!"}), 500  
      
    basic_infos = _get_info(basic_keys, user_id)
    detail_infos = _get_info(detail_keys, user_id)
    
    infos = {**basic_infos, **detail_infos}
    if not len(infos.keys()): 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Not found!"}), 500 
    return jsonify(infos), 200

@bp.route(f"/{model}/info/legal") 
@required_oauth("legal")
def find_legal_info(): 
    user_id = _check_credentials(current_token=current_token)
    if not user_id: 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "user_id required!"}), 500
    
    basic_infos = _get_info(basic_keys, user_id)
    detail_infos = _get_info(detail_keys, user_id)
    legal_infos = _get_info(legal_keys, user_id)
    
    infos = {**basic_infos, **detail_infos, **legal_infos}
    if not len(infos.keys()): 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Not found!"}), 500  
    return jsonify(infos), 200



    
    