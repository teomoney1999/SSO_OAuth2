import datetime
class Config: 
    SECRET_KEY = "ydiOMSt7RgzwElUtZtIa17cxZrKO5lN2mv4hKrJwhKvIXcUwHeFaltyn0MKG5I3q"
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
    
    # FLASK JWT EXTENDED
    JWT_SECRET_KEY = "gFW4iCMAQRsmqu0jYsazzZ1HBknRqOUy"
    JWT_TOKEN_LOCATION = ["cookies", "headers"] 
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30) 
    JWT_ERROR_MESSAGE_KEY = "error_message"
    # JWT_ALGORITHM = "HS256", 
    JWT_COOKIE_SAMESITE = "None"
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_SESSION_COOKIE = False
    # JWT_COOKIE_DOMAIN = "http://dev.localhost:3000/"
    JWT_CSRF_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    
    
   