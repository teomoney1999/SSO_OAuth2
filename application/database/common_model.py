import uuid, time 
from math import floor 
from application.database import db
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy import (
    String, BigInteger, Boolean, event, 
)

def default_uuid(): 
    return str(uuid.uuid4())

class CommonModel(db.Model): 
    __abstract__ = True
    
    id = db.Column(db.String(255), primary_key=True, default=default_uuid)
    created_at = db.Column(db.BigInteger) 
    created_by = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.BigInteger)
    updated_by = db.Column(db.String(255), nullable=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String(255), nullable=True)
    deleted_at = db.Column(db.BigInteger)


@event.listens_for(CommonModel, "before_insert")
def model_oncreate_listener(mapper, connection, target): 
    target.created_at = floor(time.time()) 

@event.listens_for(CommonModel, "before_insert")
def model_onupdate_listener(mapper, connection, target): 
    target.updated_at = floor(time.time()) 
    if target.deleted: 
        target.deleted_at = floor(time.time())
        
event.listen(CommonModel, "before_insert", model_oncreate_listener, propagate=True) 
event.listen(CommonModel, "before_update", model_onupdate_listener, propagate=True)