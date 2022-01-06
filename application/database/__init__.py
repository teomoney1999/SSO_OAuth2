from flask_sqlalchemy import SQLAlchemy

# import sys
# print("database.__init__", sys.path, __name__)

db = SQLAlchemy()

def init_database(app): 
    db.init_app(app)

