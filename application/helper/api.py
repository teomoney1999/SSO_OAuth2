

import uuid, json, time, math
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import RelationshipProperty as RelProperty
from sqlalchemy.ext.associationproxy import AssociationProxy
from application.database import db
from application.database.model import User
from application.config.cookies import Cookie
from application.controllers import USER_LOGIN, USER

def to_dict(instance): 
    # Read more about mapper: https://docs.sqlalchemy.org/en/14/orm/mapping_api.html#sqlalchemy.orm.Mapper
    # https://stackoverflow.com/questions/1958219/how-to-convert-sqlalchemy-row-object-to-a-python-dict
    return {c.key : getattr(instance, c.key) 
                for c in inspect(instance).mapper.column_attrs}

# TODO add user relationship to response
COLUMN_TYPES = (InstrumentedAttribute, hybrid_property)
RELATION_BLACKLIST = ('query', 'query_class', '_sa_class_manager',
                      '_decl_class_registry')

def get_columns(model): 
    columns = {} 
    # __mro__: Python Multiple Inheritance – Python MRO (Method Resolution Order)
    # https://data-flair.training/blogs/python-multiple-inheritance/    
    for superclass in model.__mro__: 
        for name, column in superclass.__dict__.items(): 
            print("name, col", name, column)
            # Filter all attributes without __prefix and __postfix
            if isinstance(column, COLUMN_TYPES): 
                columns[name] = column
    return columns
    
def get_relations(model):
    """Returns a list of relation names of `model` (as a list of strings)."""
    print([k for k in dir(model)
            if not (k.startswith('__') or k in RELATION_BLACKLIST)
            and get_related_model(model, k)])
    return [k for k in dir(model)
            if not (k.startswith('__') or k in RELATION_BLACKLIST)
            and get_related_model(model, k)]


def get_related_model(model, relationname):
    """Gets the class of the model to which `model` is related by the attribute
    whose name is `relationname`.

    """
    if hasattr(model, relationname):
        attr = getattr(model, relationname)
        if hasattr(attr, 'property') \
                and isinstance(attr.property, RelProperty):
            return attr.property.mapper.class_
        if isinstance(attr, AssociationProxy):
            return get_related_association_proxy_model(attr)
    return None

def get_related_association_proxy_model(attr):
    """Returns the model class specified by the given SQLAlchemy relation
    attribute, or ``None`` if no such class can be inferred.

    `attr` must be a relation attribute corresponding to an association proxy.

    """
    prop = attr.remote_attr.property
    for attribute in ('mapper', 'parent'):
        if hasattr(prop, attribute):
            return getattr(prop, attribute).class_
    return None
        
        
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