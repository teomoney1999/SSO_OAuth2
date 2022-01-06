from authlib.oauth2.rfc7662 import IntrospectionEndpoint 
from .sql_function import create_query_token_func
from application.database.model import OAuth2Token

class MyIntrospectionEndpoint(IntrospectionEndpoint): 
    def query_token(self, token, token_type_hint): 
        if token_type_hint == "access_token": 
            _token = OAuth2Token.query.filter_by(access_token=token).first()
        elif token_type_hint == "refresh_token": 
            _token = OAuth2Token.query.filter_by(refresh_token=token).first()
        else: 
            # without token type hint 
            _token = OAuth2Token.query.filter_by(access_token=token).first()
            if not _token: 
                OAuth2Token.query.filter_by(refresh_token=token).first()
        return _token
    
    def introspect_token(self, token): 
        return {
            "active": True, 
            "client_id": token.client_id,
            # "username": get_token_username,
            # "scope": token.get_scope(),
            # "sub": get_token_user_sub(token),
            "aud": token.client_id, 
            "iss": 'https://server.example.com/',
            "exp": token.expired_at, 
            "iat": token.issued_at,
        }
    
    def check_permission(self, token, client, request): 
        return client.client_type == "internal"