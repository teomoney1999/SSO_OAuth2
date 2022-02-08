

import uuid, json, time, math

from sqlalchemy.inspection import inspect
from application.database.model import User
from application.config.cookies import Cookie
from application.controllers import USER_LOGIN, USER

def to_dict(instance): 
    # Read more about mapper: https://docs.sqlalchemy.org/en/14/orm/mapping_api.html#sqlalchemy.orm.Mapper
    # https://stackoverflow.com/questions/1958219/how-to-convert-sqlalchemy-row-object-to-a-python-dict
    return {c.key : getattr(instance, c.key) 
                for c in inspect(instance).mapper.column_attrs}
    
def default_uuid(): 
    return str(uuid.uuid4())

def now(): 
    return math.floor(time.time())

    
def authorize_payload(user=None, grant=None): 
    _client_metadata = json.loads(grant.client._client_metadata)
    client = to_dict(grant.client) 
    client["client_name"] = _client_metadata.get("client_name") 
    client["request_scope"] = grant.request.scope
    return {
        # "user": user if type(user) == dict else to_dict(user), 
        "client": client, 
    }

def split_by_crlf(s):
    return [v for v in s.splitlines() if v]

def response_current_user(user=None): 
    if not user: 
        return None
    resp = {}
    resp["username"] = user.username
    return resp