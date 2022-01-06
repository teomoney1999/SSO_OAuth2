class Config: 
    SECRET_KEY = "acndefhskrmsdfgs"
    SQLALCHEMY_DATABASE_URI = "postgresql://sso_user:123456abcA@localhost:5432/sso_db_2"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTH2_REFRESH_TOKEN_GENERATOR = True
    
#     OAUTH2_TOKEN_EXPIRES_IN = {
#     'authorization_code': 864000,
#     'implicit': 3600,
#     'password': 864000,
#     'client_credentials': 864000
# }
    # OAUTH2_ACCESS_TOKEN_GENERATOR =
    # OAUTH2_ERROR_URIS = [
    #    ('invalid_client', 'https://developer.your-company.com/errors#invalid-client'),
    # other error URIs
    # ]
    CORS_HEADERS = "Content-Type"
    CORS_RESOURCES = {r"/api/*": {"origins": "*"}}
    
    WTF_CSRF_TIME_LIMIT = 3600
    WTF_CSRF_SSL_STRICT = False
    
   