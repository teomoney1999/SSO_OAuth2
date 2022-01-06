from authlib.integrations.flask_oauth2 import AuthorizationServer, ResourceProtector 
from authlib.oauth2.rfc7636 import CodeChallenge
from application.extensions.OAuth2.authorization_grant import *
from application.database.model import *
from .sql_function import *

query_client = create_query_client_func(db.session, OAuth2Client) 
save_token = create_save_token_func(db.session, OAuth2Token) 

authorization = AuthorizationServer(
                    query_client=query_client, 
                    save_token=save_token)
required_oauth = ResourceProtector()

def config_oauth(app): 
    authorization.init_app(app) 
    
    # supported grant 
    authorization.register_grant(AuthorizationCodeGrant, [CodeChallenge(required=True)])
    authorization.register_grant(ImplicitGrant) 
    authorization.register_grant(ClientCredentialsGrant)
    authorization.register_grant(PasswordGrant) 
    authorization.register_grant(RefreshTokenGrant)
    
    
    # revocation_endpoint
    revocation_cls = create_revocation_endpoint(db.session, OAuth2Token)
    authorization.register_endpoint(revocation_cls)
    
    # protect resource 
    bearer_cls = create_bearer_token_validator(db.session, OAuth2Token) 
    required_oauth.register_token_validator(bearer_cls())
