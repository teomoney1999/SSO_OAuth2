from flask import (
    Blueprint, request, redirect, session, url_for,
    jsonify, render_template)
from application.database.model import User
# from application.models.user import User
from application.extensions.OAuth2.authorization_server import authorization
from authlib.oauth2 import OAuth2Error
from authlib.integrations.flask_oauth2 import current_token
from application.helper.api import to_dict

bp_oauth2 = Blueprint("oauth2", __name__)

def current_user(): 
    if "id" in session: 
        uid = session["id"] 
        return User.query.get(uid) 
    return None 

@bp_oauth2.route("/home", methods=["GET"])
def greeting(): 
    return "Welcome!"

# Authorization Endpoint
@bp_oauth2.route("/authorize", methods=["GET", "POST"]) 
def authorize(): 
    user = current_user()
    
    if not user: 
        # return "Login required!"
        return redirect(url_for('home.home', next=request.url))
    if request.method == "GET": 
        try: 
            grant = authorization.validate_consent_request(end_user=user)
        except OAuth2Error as error: 
            return error.error
        return render_template('authorize.html', user=user, grant=grant)

    # POST
    if not user and "username" in request.form: 
        username = request.form.get("username") 
        user = User.query.filter_by(username=username).first() 
    if request.form["confirm"]: 
        grant_user = user 
    else: 
        grant_user = None 
    return authorization.create_authorization_response(grant_user=grant_user)


# Token endpoint
@bp_oauth2.route("/token", methods=["POST"]) 
def issue_token(): 
    return authorization.create_token_response()

# Revocation endpoint 
@bp_oauth2.route("/revoke", methods=["POST"]) 
def revoke_token(): 
    return authorization.create_endpoint_response("revocation")

@bp_oauth2.route("/api/me") 
def api_me(): 
    user = current_token.user
    return jsonify(id=user.id, username=user.username)

grant = ['AUTHORIZATION_CODE_LENGTH', 'ERROR_RESPONSE_FRAGMENT', 'GRANT_TYPE', 
     'RESPONSE_TYPES', 'TOKEN_ENDPOINT_AUTH_METHODS', 'TOKEN_ENDPOINT_HTTP_METHODS', 
     'TOKEN_RESPONSE_HEADER', 'authenticate_token_endpoint_client', 'authenticate_user', 
     'check_authorization_endpoint', 'check_token_endpoint', 'client', 'create_authorization_response', 
     'create_token_response', 'delete_authorization_code', 'execute_hook', 'generate_authorization_code', 
     'generate_token', 'prompt', 'query_authorization_code', 'register_hook', 'request', 'save_authorization_code', 
     'save_token', 'server', 'validate_authorization_redirect_uri', 'validate_authorization_request', 
     'validate_consent_request', 'validate_requested_scope', 'validate_token_request']