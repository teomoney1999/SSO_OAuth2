from flask import Flask 
from flask_cors import CORS
from application.config.stagging import Config as Stagging
from application.database import init_database
# # from application.database.model import *
from application.controllers import init_controllers
from application.extensions import init_extensions

app = Flask(__name__)
app.config.from_object(Stagging)
CORS(app, automatic_options=True, supports_credentials=True)

init_database(app)
init_extensions(app)
init_controllers(app)

