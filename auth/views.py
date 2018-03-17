import os  # main
from flask import Flask, render_template, redirect, Blueprint


auth = Flask(__name__)
auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates', static_folder='static',
                           static_url_path='/static/')
