
from flask_wtf.csrf import CSRFProtect 
import application.extensions.OAuth2
from application.extensions.OAuth2.authorization_server import config_oauth

csrf = CSRFProtect()

def init_extensions(app): 
    # csrf.init_app(app) 
    config_oauth(app)

