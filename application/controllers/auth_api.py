from math import floor 
from datetime import datetime, timedelta
from flask import (
    Blueprint, request, redirect, session, url_for,
    jsonify, render_template, make_response)
from werkzeug.security import gen_salt
from authlib.oauth2 import OAuth2Error
from authlib.integrations.flask_oauth2 import current_token
from application.controllers import USER_LOGIN, USER
from application.database import db
from application.database.model import OAuth2Client, User
from application.extensions.OAuth2.authorization_server import authorization, required_oauth
from application.helper.api import *
from application.config.cookies import Cookie

bp = Blueprint("oauth2_api", __name__)

oauth2 = "/oauth2"

# USER_LOGIN = {
#     "dc4c7465-385c-48a2-832a-c1e86043ce90": {
#         "user_id": "dc4c7465-385c-48a2-832a-c1e86043ce90", 
#         "token": "token", 
#         "expires_time": ""
#         "expired": ""        
#     },    
# } 

# TODO: write a worker that clear token that has been expired in USER_LOGIN
@bp.route("/current_user")
def get_current_user(): 
    cookies = request.cookies
    print("cookies", cookies.get("token"))
    if not cookies.get("token"): 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Token does not exist in Cookies!"}), 500
    
    token = cookies.get("token")
    user_login = USER_LOGIN.get(token)
    if not user_login: 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Token does not exist in USER_LOGIN!"}), 500

    user = User.query.get(user_login["user_id"])
    if not user: 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Token does not represent any user in database!"}), 500
    
    return jsonify(cookies=cookies), 200


    
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
    
    # if is_duplicate_user_id(user.id): 
    #     return "OK", 200
    
    token = default_uuid()
    resp = make_response(response_current_user(user=user)) 
    resp.set_cookie(key=Cookie.KEY, value=token, max_age=Cookie.MAX_AGE, samesite=Cookie.SAMESITE, secure=Cookie.SECURE, httponly=Cookie.HTTPONLY)
          
    user_login = {  "user_id": user.id, 
                    "token": token, 
                    "expires_time": floor((datetime.now()+ timedelta(seconds=Cookie.MAX_AGE)).timestamp()), 
                    "expired": False }
    USER_LOGIN[f"{token}"] = user_login
    # USER.append(user.id)
    session["token"] = user_login.get("token")
    print("USER_LOGIN", USER_LOGIN)
    return resp, 200

@bp.route(f"/logout", methods=["GET"]) 
def logout(): 
    resp = make_response({})
    token = request.cookies.get("token")
    print("token", token)
    if not token: 
        return resp, 200
    
    if USER_LOGIN.get(token):
        # remove user_id in USER
        # user_id = USER_LOGIN[token]["user_id"] 
        # USER.remove(user_id)
        # remove token key in USER_LOGIN
        del USER_LOGIN[token]
        # delete cookie 
        resp.delete_cookie("token")
    print("USER_LOGIN", USER_LOGIN)
    return resp, 200
        

@bp.route(f"/oauth2/authorize", methods=("GET", "POST"))
def authorize():
    user = current_user(session=session, request=request) 
    print("USER_LOGIN", user)
    # TODO: delete this after testing
    # user = User.query.get('dc4c7465-385c-48a2-832a-c1e86043ce90')
    if not user: 
        return jsonify({"error_code": "ACCESS_DENIED", "error_message": "Login required!"}), 500
    if request.method == "GET":
        try: 
            # print("request", request.json)
            grant = authorization.validate_consent_request(end_user=user) 
        except OAuth2Error as error: 
            return jsonify({"error_code": "OAUTH_ERROR", "error_message": f"{error.error}"})
        return jsonify(authorize_payload(user, grant))
    # POST method use for take resource owner confirmation
    data = request.json
    if not data: 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Need confirmation from Resource Owner!"}), 500
    if "confirm" not in data: 
        return jsonify({"error_code": "PARAM_ERROR", "error_message": "Can not get confirmation from Resource Owner!"}), 500
    if data.get("confirm") is not True: 
        return jsonify({"error_code": "ACCESS_DENIED", "error_message": "Resource Owner does not allow your request!"}), 500
    return authorization.create_authorization_response(grant_user=user) 


@bp.route("/oauth2/token", methods=["POST"])
def issue_token(): 
    return authorization.create_token_response()


@bp.route("/user") 
@required_oauth("profile")
def find(): 
    user = current_token.user
    return jsonify(username=user.username)
    # data = request.json 
    
    # if "username" in data: 
    #     return jsonify(to_dict(User.query.filter_by(username=data["username"]).first())), 200
    
    # return jsonify({"error_code": "PARAM_ERROR", "error_message": "Not found!"}), 500  
    
        
        