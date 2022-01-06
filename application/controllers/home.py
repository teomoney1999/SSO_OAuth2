import time
from flask import (
    Blueprint, request, redirect, session, url_for,
    jsonify, render_template)
from werkzeug.security import gen_salt
from application.database import db
from application.database.model import User, OAuth2Client
# from application.models.user import User
from application.extensions.OAuth2.authorization_server import authorization, required_oauth
from authlib.oauth2 import OAuth2Error
from authlib.integrations.flask_oauth2 import current_token
from application.controllers.auth import current_user



bp_home = Blueprint("home", __name__) 

def split_by_crlf(s):
    return [v for v in s.splitlines() if v]

CLIENT_METADATA = {
    "client_name": None, 
    "client_uri": None, 
    "grant_types": [], 
    "redirect_uris": [], 
    "response_types": [], 
    "scope": None, 
    "token_endpoint_auth_method": None}

@bp_home.route("/", methods=("GET", "POST")) 
def home(): 
    if request.method == "POST": 
        username = request.form.get("username") 
        user = User.query.filter_by(username=username).first() 
        if not user: 
            user = User(username=username) 
            db.session.add(user)
            db.session.commit() 
        
        session["id"] = user.id
        # if user is not just to log in, 
        # but need to head back to auth page 
        next_page = request.args.get("next") 
        if next_page:
            return redirect(next_page)
        return redirect("/")
    user = current_user() 
    if user: 
        clients = OAuth2Client.query.filter_by(user_id=user.id).all() 
    else: 
        clients = [] 
    
    return render_template("home.html", user=user, clients=clients)


@bp_home.route("/create_client", methods=("GET", "POST")) 
def create_client(): 
    user = current_user() 
    if not user: 
        return redirect("/") 
    if request.method == "GET": 
        return render_template("create_client.html") 
    
    client_id = gen_salt(24)
    client_id_issued_at = int(time.time()) 
    client = OAuth2Client(
        client_id=client_id, 
        client_id_issued_at=client_id_issued_at,
        user_id=user.id
    )
    form = request.form 
    client_metadata = {
        "client_name": form["client_name"],
        "client_uri": form["client_uri"],
        "grant_types": split_by_crlf(form["grant_type"]),
        "redirect_uris": split_by_crlf(form["redirect_uri"]),
        "response_types": split_by_crlf(form["response_type"]),
        "scope": form["scope"],
        "token_endpoint_auth_method": form["token_endpoint_auth_method"]
    }
    client.set_client_metadata(client_metadata)
    # client_metadata = CLIENT_METADATA
    # for key in client_metadata: 
    #     if type(client_metadata[key]) is list: 
    #         client_metadata[key] = split_by_crlf(form[key])
    #         continue
    #     client_metadata[key] = form[key]
    # print("client_metadata", client_metadata)
    # client.set_client_metadata(client_metadata)
    
    if form["token_endpoint_auth_method"] == "none": 
        client.client_secret = "" 
    else: 
        client.client_secret = gen_salt(48)
    
    db.session.add(client) 
    db.session.commit()
    return redirect('/')

@bp_home.route("/login", methods=["GET", "POST"]) 
def login(): 
    username = request.form.get("username") 
    password = request.form.get("password")
    
    user = User.query.filter_by(username=username).first()
    if not user: 
        return f"User {username} does not exist", 500
    session['id'] = user.id
    return "Login successfully", 200
    

@bp_home.route("/logout") 
def logout(): 
    print("=====session", session)
    del session["id"] 
    return redirect("/")

@bp_home.route('/api/me')
@required_oauth('profile')
def api_me():
    user = current_token.user
    return jsonify(id=user.id, username=user.username)