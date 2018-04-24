from app import app
from flask import render_template, redirect
from flask_restful import reqparse
from models import UserModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)



parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)
parser.add_argument('first_name', help = 'This field cannot be blank', required = True)
parser.add_argument('last_name', help = 'This field cannot be blank', required = True)
parser.add_argument('contact_number', help = 'This field cannot be blank', required = True)
parser.add_argument('birth_date', help = 'This field cannot be blank', required = True)
parser.add_argument('gender', help = 'This field cannot be blank', required = True)



@app.route('/')
def index():
   # return jsonify({'message': 'Hello World!'})
    return render_template('landing.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/signin')
def signin():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('registration.html')

# @app.route('/logout')
# @jwt_required
# def logout():
#     jti = get_raw_jwt()['jti']
#     try:
#         revoked_token = RevokedTokenModel(jti=jti)
#         revoked_token.add()
#        # return {'message': 'Access token has been revoked'}
#         return render_template('dashboard.html')
#     except:
#         return {'message': 'Something went wrong'}, 500


# @app.route('/registration', methods=['GET','POST'])
# def register():
#     data = parser.parse_args()
#
#     if UserModel.find_by_username(data['username']):
#         return ("User {} already exists".format(data['username']))
#
#     new_user = UserModel(
#         username=data['username'],
#         password=UserModel.generate_hash(data['password']),
#         first_name=data['first_name'],
#         last_name=data['last_name'],
#         contact_number=data['contact_number'],
#         birth_date=data['birth_date'],
#         gender=data['gender']
#     )
#
#     try:
#         new_user.save_to_db()
#         access_token = create_access_token(identity=data['username'])
#         refresh_token = create_refresh_token(identity=data['username'])
#
#         # return ("User was created. Tokens are %s and %s" % (access_token, refresh_token))
#         return render_template('dashboard.html', access_token=access_token, refresh_token=refresh_token)
#     except:
#         return ("Something went wrong", 500)
#



