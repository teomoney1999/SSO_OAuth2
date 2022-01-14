import time
from application.database import db 
from application.database.common_model import CommonModel
from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin, OAuth2TokenMixin, OAuth2AuthorizationCodeMixin)
from authlib.oauth2.rfc6749 import grants

# import sys
# print("model.py: ", sys.path, __name__)

## RESOURCE OWNER is the user using our service
class User(CommonModel): 
    username = db.Column(db.String(255), unique=True) 
    password = db.Column(db.String(255)) 
    salt = db.Column(db.String(255)) 
    status = db.Column(db.SmallInteger()) 
    last_login_at = db.Column(db.BigInteger())

    def __str__(self): 
        return self.username 
    
    def get_user_id(self): 
        return self.id 
    
    def check_password(self, password): 
        return password == "valid" 

class UserInfo(CommonModel): 
    __tablename__ = "userinfo" 
    id_number = db.Column(db.String(255)) 
    previous_id_number = db.Column(db.String(255))
    full_name = db.Column(db.String(255)) 
    date_birth = db.Column(db.BigInteger)       # timestamp
    gender = db.Column(db.SmallInteger, default=0) # 0 is male, 1 is woman
    address = db.Column(db.String(255)) 
    district = db.Column(db.String(255)) 
    province = db.Column(db.String(255)) 
    ward = db.Column(db.String(255)) 
    date_register = db.Column(db.BigInteger)    # timestamp
    
    user_id = db.Column(db.String(255),
                        db.ForeignKey("user.id", ondelete="CASCADE"))
    user = db.relationship("User") 
    


## CLIENT is an application making protected resource 
# requests on behalf of the resource owner
class OAuth2Client(CommonModel, OAuth2ClientMixin): 
    # client_id: Client Identifier
    # client_secret: Client Password
    # Client Token Endpoint Authentication Method
    user_id = db.Column(db.String(255),
                        db.ForeignKey("user.id", ondelete="CASCADE"))
    user = db.relationship("User") 
    

## TOKEN is used to accesss the user's resources
class OAuth2Token(CommonModel, OAuth2TokenMixin): 
    # access_token: a token to authorize the http requests
    # refresh_token: (optional) a token to exchange a new access token
    # client_id: this token is issued to which client
    # expires_at: expired time of an token
    # scope: a limited scope of resources that this token can access
    user_id = db.Column(db.String(255),
                        db.ForeignKey("user.id", ondelete="CASCADE"))
    user = db.relationship("User") 
    
    def is_refresh_token_active(self): 
        if self.revoked: 
            return False 
        expires_at = self.issue_at + self.expires_in * 2
        return expires_at >= time.time()
    
    
## AUTHORIZATION CODE GRANT
class OAuth2AuthorizationCode(CommonModel, OAuth2AuthorizationCodeMixin): 
    user_id = db.Column(db.String(255),
                        db.ForeignKey("user.id", ondelete="CASCADE"))
    user = db.relationship("User") 

