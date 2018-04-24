from app import app
from flask import render_template, request
from flask_restful import reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import requests


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

@app.route('/signuup')
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(
            'http://localhost:8080/login',
            json={"username": username, "password": password, },
            auth=(username, password),
        )
        try:
            access_token = create_access_token(identity=request.form['username'])
            refresh_token = create_refresh_token(identity=request.form['username'])

            return ("User was created. Tokens are %s and %s" % (access_token, refresh_token))
            #return render_template('dashboard.html', access_token=access_token, refresh_token=refresh_token)
        except:
            return ("Something went wrong", 500)
    else:
        return render_template('login.html')
    # print(response.text)
    # if response.text == "Could not verify":
    #     return render_template('landing.html')

    # return render_template('dashboard.html')
    # return ("User was created. Tokens are %s and %s" % (access_token, refresh_token))


@app.route('/registration', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        contact_number=request.form['contact_number'],
        birth_date=request.form['birth_date'],
        gender=request.form['gender']
        requests.post(
            'http://localhost:8080/signup',
            json={"first_name": first_name, "last_name": last_name,
                  "birth_date": birth_date, "gender": gender,
                  "contact_number": contact_number, "username": username, "password": password}
        )

        try:
            access_token = create_access_token(identity=request.form['username'])
            refresh_token = create_refresh_token(identity=request.form['username'])

            #return ("User was created. Tokens are %s and %s" % (access_token, refresh_token))
            return render_template('dashboard.html', access_token=access_token, refresh_token=refresh_token)
        except:
            return ("Something went wrong", 500)

    else:
        return render_template('landing.html')







