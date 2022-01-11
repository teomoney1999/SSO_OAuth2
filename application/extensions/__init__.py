
from flask_wtf.csrf import CSRFProtect 
import application.extensions.OAuth2
from flask_jwt_extended import JWTManager
from application.extensions.OAuth2.authorization_server import config_oauth

csrf = CSRFProtect()

jwt = JWTManager() 
def init_extensions(app): 
    # csrf.init_app(app) 
    config_oauth(app)
    
    jwt.init_app(app)

