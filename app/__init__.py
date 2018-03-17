from flask import Flask
from flask_sqlalchemy import SQLAlchemy, SessionBase
from flask_bootstrap import Bootstrap
import datetime


app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_pyfile('config.py')
bootstrap = Bootstrap(app)

from models import *
from forms import *
from app import view

db.create_all()
